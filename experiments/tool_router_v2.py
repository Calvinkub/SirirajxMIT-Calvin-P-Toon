"""Tool router v2: frequent-phrase rules -> one-pass LLM scoring (+cached prefix) + hidden-state probe -> agree-or-clarify.

SYNTHETIC DATA. Train: synthetic/router_train.jsonl (+ v1 72 rows). Test: synthetic/router_test_blind.jsonl,
written by a separate agent that never saw the rules, the train set or this code. Rules and thresholds are
frozen before the test file is read (see FROZEN_* below and the git history).

    python experiments/tool_router_v2.py --model Qwen/Qwen3-1.7B
"""

import argparse
import copy
import json
import re
import statistics
import time
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "synthetic"

LABELS = ["search_places", "search_activities", "get_heat_index", "get_pm25", "get_patient_limits",
          "get_recent_activity", "log_checkin", "none"]  # red_flag is rules-only, never scored by a model
DESC = {
    "search_places": "a place to walk or exercise alone: park, temple, mall, track / หาที่เดิน สวน วัด ห้าง",
    "search_activities": "a group, class, club or people to exercise with / หากลุ่ม คลาส เพื่อนออกกำลัง",
    "get_heat_index": "temperature, heat, sun, rain, weather / อากาศร้อนไหม ฝนตกไหม",
    "get_pm25": "air quality, dust, smoke, PM2.5, mask / ฝุ่น ควัน PM2.5",
    "get_patient_limits": "what they are allowed to do: heart-rate limit, how hard, which activities / หมอให้ทำได้แค่ไหน",
    "get_recent_activity": "see their own past steps, heart rate, progress / ดูก้าว ชีพจร ความคืบหน้า",
    "log_checkin": "report how a mission went, did or skipped it, took medicine / รายงานว่าเดินแล้ว รู้สึกยังไง",
    "none": "greeting, thanks, app questions, ANY medicine question, general medical questions / ทักทาย ถามเรื่องยา",
}
LETTERS = "ABCDEFGH"

# ---------- Tier 0: safety rules (deterministic) ----------
NEG = r"(ไม่(ได้|มี)?|ไม่เคย|no|not|don'?t|didn'?t|without|never|ไม่ค่อย)"
RED_FLAG = re.compile(
    r"chest.{0,15}(pain|tight|pressure|hurt|heavy|squeez)|(pain|tight|pressure|heavy).{0,10}chest|"
    r"can'?t (catch my breath|breathe)|short(ness)? of breath|breathless|out of breath|gasp|"
    r"dizz|light-?headed|faint|pass(ed)? out|black(ed)? out|room (is )?spinning|"
    r"palpitat|heart.{0,12}(racing|skipp|pound|flutter|irregular|beating fast)|"
    r"(arm|jaw|back|shoulder).{0,15}(pain|hurt|numb)|pain.{0,25}(arm|jaw)|cold sweat|sweat(y|ing)?.{0,12}cold|"
    r"เจ็บ.{0,10}(หน้า|กลาง)?อก|กลางอก|แน่น.{0,6}(หน้า)?อก|จุก.{0,4}อก|อึดอัด.{0,4}(หน้า)?อก|บีบ.{0,4}(หัวใจ|อก)|"
    r"หายใจไม่(ออก|ทัน|อิ่ม|สะดวก)|หอบ|"
    r"เวียน(หัว|ศีรษะ)|มึน(หัว)?|หน้ามืด|เป็นลม|จะเป็นลม|วูบ|"
    r"ใจสั่น|ใจเต้น(แรง|เร็ว|ผิด|ไม่เป็น)|หัวใจเต้น(แรง|เร็ว|ผิด|รัว)|"
    r"(ร้าว|ชา).{0,6}(แขน|กราม|ไหล่|หลัง)|เหงื่อ(ออก|แตก).{0,6}(เย็น|ท่วม)", re.I)
GENERAL_Q = re.compile(r"(what|which) (are|is) (the )?(sign|symptom)|อาการ.{0,10}(คือ|เป็นยังไง|มีอะไรบ้าง)|สัญญาณเตือน", re.I)
MEDICATION = re.compile(
    r"(medic|medicine|pill|tablet|dose|drug|bisoprolol|metoprolol|aspirin|clopidogrel|ticagrelor|statin|nitro|"
    r"side effect)|(กิน|ทาน|ลืม|หยุด|เพิ่ม|ลด|เลิก|เปลี่ยน|งด)ยา|ยา(ตัว|เม็ด|ลด|ละลาย|ขยาย|ความดัน|เบาหวาน|ไขมัน|หัวใจ|อมใต้ลิ้น)|ยาที่|ผลข้างเคียง", re.I)
MED_REPORT = re.compile(r"(took|taken|have taken|กินยา.{0,20}(แล้ว|เรียบร้อย|ครบ))", re.I)


def denied(text, m):
    return re.search(NEG + r"\s?.{0,6}$", text[max(0, m.start() - 12):m.start()], re.I) is not None


def safety_rules(text):
    m = RED_FLAG.search(text)
    if m and not denied(text, m) and not GENERAL_Q.search(text):
        return "red_flag"
    if MEDICATION.search(text) and not MED_REPORT.search(text):
        return "none"
    return None


# ---------- Tier 1: frequent-phrase rules (fire only when exactly one label matches) ----------
FREQUENT = {
    "get_pm25": r"pm ?2\.?5|\bpm\b|ฝุ่น|ควัน|หมอกควัน|haze|smog|smoke|dust|air quality|คุณภาพอากาศ|aqi|หน้ากาก(อนามัย|กันฝุ่น)?|mask",
    "get_heat_index": r"ร้อน|อบอ้าว|อุณหภูมิ|องศา|แดด|อากาศ(เย็น|ดี|เป็นยังไง)|hot|heat|temperature|degrees|sunny|weather|cool(er)? (outside|today|later)",
    "search_activities": r"กลุ่ม|ก๊วน|ชมรม|คลาส|ไทชิ|ไท้เก๊ก|รำไม้พลอง|แอโรบิ(ค|ก)|(?<!ใจ)เต้น|เพื่อน.{0,6}(เดิน|ออกกำลัง)|ไปด้วยกัน|group|club|class|tai ?chi|together|join|buddy|rehab (class|session)",
    "search_places": r"สวน(สาธารณะ)?|วัด|ห้าง|ลู่วิ่ง|ลู่เดิน|ที่(ไหน)?.{0,4}เดิน|เดิน.{0,6}ที่ไหน|park|temple|mall|track|where (can|could|should) i (walk|go)|place to walk|route",
    "get_patient_limits": r"หลังผ่าตัด|ผ่าตัด.{0,20}(ได้|หรือยัง)|หมอ.{0,8}(ให้|อนุญาต|บอก)|หนักแค่ไหน|เกินเท่าไหร่|ยกของ.{0,10}(ได้|หรือยัง)|allowed|can i (lift|swim|cycle|ride|run|jog)|how hard|limit|heart rate (should|max|limit)|ceiling",
    "get_recent_activity": r"so far|on track|this (week|month).{0,20}(complet|done|did)|(กี่|จำนวน)ก้าว|ก้าว.{0,6}(เท่าไหร่|กี่)|ความคืบหน้า|สถิติ|ย้อนหลัง|สัปดาห์นี้.{0,10}(เดิน|ก้าว)|ชีพจร.{0,10}(ที่ผ่านมา|ย้อนหลัง|เป็นยังไง)|how many steps|my steps|progress|history|last (week|few days)|show (me )?my|resting heart rate (was|over)",
    "log_checkin": r"เมื่อ(เช้า|เย็น|วาน|กี้)|ไป ?\d+ ?(นาที|รอบ)|\d+ ?รอบ|ไม่ได้ออกไป|เดินรอบ|เดิน(เสร็จ|ครบ|แล้ว)|วันนี้(ไม่ได้)?เดิน|ข้าม|รู้สึก(ดี|สบาย|เหนื่อย)|ทำ(เสร็จ|ครบ)แล้ว|กินยา(แล้ว|เรียบร้อย)|finished|done (my|with)|completed|skipped|did my walk|felt (easy|good|hard|fine)|took my",
    "none": r"^(สวัสดี|หวัดดี|ขอบคุณ|thank|thanks|hi|hello|good (morning|night))|sync|เชื่อม.{0,10}นาฬิกา|(กิน|ดื่ม)(กาแฟ|เหล้า|เบียร์|ชา)|แอป(นี้)?.{0,8}(ใช้|ทำ)|ใครทำ|who made|how (do i )?use (this|the) app|joke|เล่นมุก",
}
FREQUENT = {k: re.compile(v, re.I) for k, v in FREQUENT.items()}


QUESTION = re.compile(r"\?|ไหม|มั้ย|เท่าไหร่|เท่าไร|กี่|ขอดู|หรือเปล่า|รึเปล่า|จำไม่ได้|^(what|how|did|do|was|is|am)\b", re.I)


def frequent_rules(text):
    hits = [k for k, rx in FREQUENT.items() if rx.search(text)]
    if "log_checkin" in hits and QUESTION.search(text):
        hits.remove("log_checkin")  # a question about the past is a lookup, not a report
    return hits[0] if len(hits) == 1 else None


# ---------- Tier 2 + 3: one forward pass gives letter scores AND hidden-state features ----------
class OnePass:
    def __init__(self, model_id, fewshot):
        self.tok = AutoTokenizer.from_pretrained(model_id)
        self.dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        self.model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32 if self.dev == "cpu" else torch.float16).to(self.dev).eval()
        menu = "\n".join(f"{LETTERS[i]}. {lab}: {DESC[lab]}" for i, lab in enumerate(LABELS))
        shots = "\n".join(f"Message: {r['text']}\nAnswer: {LETTERS[LABELS.index(r['tool'])]}" for r in fewshot)
        marker = "<<<MSG>>>"
        user = (f"Classify a Thai heart patient's message into one option.\n{menu}\n\nExamples:\n{shots}\n\n"
                f"Message: {marker}\nAnswer with one letter.")
        full = self.tok.apply_chat_template([{"role": "user", "content": user}], add_generation_prompt=True,
                                            tokenize=False, enable_thinking=False)
        self.prefix, self.suffix_tpl = full.split(marker)
        pre = self.tok(self.prefix, return_tensors="pt").to(self.dev)
        with torch.no_grad():
            self.cache = self.model(**pre, use_cache=True).past_key_values  # computed once, reused per message
        self.pre_len = pre["input_ids"].shape[1]
        self.letter_ids = [self.tok.encode(c, add_special_tokens=False)[0] for c in LETTERS[:len(LABELS)]]
        self.prefix_tokens = self.pre_len

    def __call__(self, text):
        ids = self.tok(text + self.suffix_tpl, return_tensors="pt", add_special_tokens=False).to(self.dev)
        n_msg = len(self.tok(text, add_special_tokens=False)["input_ids"])
        cache = copy.deepcopy(self.cache)
        with torch.no_grad():
            out = self.model(input_ids=ids["input_ids"], past_key_values=cache, use_cache=True, output_hidden_states=True)
        logits = out.logits[0, -1, self.letter_ids].float()
        probs = torch.softmax(logits, -1).cpu().numpy()
        hs = out.hidden_states
        layers = [len(hs) // 2, (3 * len(hs)) // 4, len(hs) - 1]
        feat = torch.cat([hs[l][0, :max(1, n_msg)].float().mean(0) for l in layers]).cpu().numpy()
        return probs, feat


def sync(dev):
    if dev == "cuda":
        torch.cuda.synchronize()
    elif dev == "mps":
        torch.mps.synchronize()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-1.7B")
    ap.add_argument("--tau", type=float, default=None, help="override the CV-chosen threshold")
    a = ap.parse_args()
    read = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    train = read(SYN / "router_train.jsonl") + read(SYN / "tool_router_utterances.jsonl")
    test = read(SYN / "router_test_blind.jsonl")

    rng = np.random.default_rng(0)
    fewshot = []
    for lab in LABELS:  # 2 shots per label, from train only
        pool = [r for r in train if r["tool"] == lab]
        fewshot += [pool[i] for i in rng.choice(len(pool), 2, replace=False)]
    op = OnePass(a.model, fewshot)
    for _ in range(3):
        op("hello")

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    tr = [r for r in train if r["tool"] in LABELS and r not in fewshot]
    Ptr, Ftr = zip(*(op(r["text"]) for r in tr))
    ytr = np.array([LABELS.index(r["tool"]) for r in tr])
    probe = make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=3000))
    cv_probs = cross_val_predict(probe, np.array(Ftr), ytr, cv=5, method="predict_proba")
    probe.fit(np.array(Ftr), ytr)

    def decide(p_llm, p_probe, tau):
        ens = (p_llm + p_probe) / 2
        top = int(np.argmax(ens))
        agree = int(np.argmax(p_llm)) == int(np.argmax(p_probe)) == top
        return (top if agree and ens[top] >= tau else None), ens

    # choose tau on TRAIN (cross-validated probe) only: smallest tau with >= 99.5% selective accuracy
    tau = a.tau
    if tau is None:
        tau = 0.95
        for t in np.arange(0.30, 0.96, 0.01):
            picks = [(decide(np.array(p), cp, t)[0], y) for p, cp, y in zip(Ptr, cv_probs, ytr)]
            acc = [d == y for d, y in picks if d is not None]
            if acc and np.mean(acc) >= 0.995:
                tau = float(round(t, 2))
                break

    rows, times, tiers = [], [], {"safety": 0, "frequent": 0, "model": 0, "clarify": 0}
    for r in test:
        sync(op.dev); t0 = time.perf_counter()
        pred, tier, top2 = safety_rules(r["text"]), "safety", None
        if pred is None:
            pred, tier = frequent_rules(r["text"]), "frequent"
        if pred is None:
            p_llm, f = op(r["text"])
            d, ens = decide(p_llm, probe.predict_proba(f[None])[0], tau)
            top2 = [LABELS[i] for i in np.argsort(-ens)[:2]]
            pred, tier = (LABELS[d], "model") if d is not None else ("CLARIFY", "clarify")
        sync(op.dev); times.append(time.perf_counter() - t0)
        tiers[tier] += 1
        rows.append({"id": r["id"], "gold": r["tool"], "pred": pred, "tier": tier, "top2": top2})

    n = len(rows)
    answered = [x for x in rows if x["pred"] != "CLARIFY"]
    clar = [x for x in rows if x["pred"] == "CLARIFY"]
    red = [x for x in rows if x["gold"] == "red_flag"]
    res = {
        "meta": {"model": a.model, "device": op.dev, "gpu": torch.cuda.get_device_name(0) if op.dev == "cuda" else None,
                 "train_rows": len(train), "test_rows": n, "tau": tau, "prefix_tokens_cached": op.prefix_tokens,
                 "data_origin": "synthetic; test written blind by a separate agent", "date": time.strftime("%Y-%m-%d")},
        "selective_accuracy": round(np.mean([x["pred"] == x["gold"] for x in answered]), 4) if answered else None,
        "coverage": round(len(answered) / n, 4),
        "accuracy_if_clarify_counts_wrong": round(np.mean([x["pred"] == x["gold"] for x in rows]), 4),
        "clarify_top2_contains_gold": round(np.mean([x["gold"] in (x["top2"] or []) for x in clar]), 4) if clar else None,
        "accuracy_after_two_option_clarify": round(np.mean([(x["pred"] == x["gold"]) or (x["pred"] == "CLARIFY" and x["gold"] in (x["top2"] or [])) for x in rows]), 4),
        "red_flag_recall": round(np.mean([x["pred"] == "red_flag" for x in red]), 4),
        "red_flag_false_alarms": sum(x["pred"] == "red_flag" and x["gold"] != "red_flag" for x in rows),
        "tier_counts": tiers,
        "median_ms": round(statistics.median(times) * 1000, 1), "p95_ms": round(sorted(times)[int(0.95 * (n - 1))] * 1000, 1),
        "errors": [x for x in rows if x["pred"] not in ("CLARIFY", x["gold"])],
    }
    out = ROOT / "experiments" / f"tool_router_v2_results_{a.model.split('/')[-1]}_{op.dev}.json"
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "errors"}, indent=2, ensure_ascii=False))
    print("errors:", len(res["errors"]))


if __name__ == "__main__":
    main()
