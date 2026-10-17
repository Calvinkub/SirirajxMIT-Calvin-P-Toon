"""Quick hackathon demo: plain LLM tool calling vs a rules + one-pass router.

SYNTHETIC DATA ONLY (synthetic/tool_router_utterances.jsonl, written by the team's
assistant). Numbers from this script show the mechanism, not real-world accuracy.

    python3 experiments/tool_router_demo.py [--model Qwen/Qwen3-0.6B] [--limit N]
"""

import argparse
import json
import re
import statistics
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "synthetic" / "tool_router_utterances.jsonl"

TOOLS = {
    "search_places": "Find a nearby place to walk: park, temple, indoor mall or track.",
    "search_activities": "Find a group activity or class: walking group, tai chi, rehab class.",
    "get_heat_index": "Get current or later heat and temperature for the patient's district.",
    "get_pm25": "Get current PM2.5 dust and air quality for the patient's district.",
    "get_patient_limits": "Read the clinician-set exercise limits: heart-rate ceiling, effort, allowed activities.",
    "get_recent_activity": "Read recent steps, heart rate and missions from the watch.",
    "log_checkin": "Record how a finished or skipped mission felt.",
    "none": "No tool: greetings, small talk, questions about the app.",
}
LETTERS = "ABCDEFGH"

# Rules tier (deterministic). Written with knowledge of this synthetic set, so it is optimistic.
RED_FLAG = re.compile(r"chest.{0,12}(pain|tight|pressure)|tight.{0,6}chest|can'?t (catch|breathe)|short(ness)? of breath|breathless|"
                      r"dizz|light-?headed|faint|passed out|palpitat|heart.{0,10}(racing|skipp|pounding)|"
                      r"เจ็บ.{0,4}หน้าอก|แน่น.{0,4}หน้าอก|หายใจไม่(ออก|ทัน)|เหนื่อยหอบ|เวียนหัว|หน้ามืด|เป็นลม|ใจสั่น|ใจเต้น(แรง|ผิด)", re.I)
MEDICATION = re.compile(r"(stop|skip|double|extra).{0,20}(medic|pill|tablet|bisoprolol|metoprolol|aspirin)|"
                        r"(ลืม|หยุด|เพิ่ม).{0,10}ยา|กินยา.{0,6}(เพิ่ม|ไหม)", re.I)


def load(model_id):
    tok = AutoTokenizer.from_pretrained(model_id)
    dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32 if dev == "cpu" else torch.float16).to(dev).eval()
    return tok, model, dev


def sync(dev):
    if dev == "mps":
        torch.mps.synchronize()
    elif dev == "cuda":
        torch.cuda.synchronize()


def baseline(tok, model, dev, text):
    """Native tool calling: the model writes the whole <tool_call> JSON."""
    tools = [{"type": "function", "function": {"name": n, "description": d, "parameters": {"type": "object", "properties": {}}}}
             for n, d in TOOLS.items() if n != "none"]
    msgs = [{"role": "system", "content": "You help heart patients. Call one tool if needed, otherwise reply briefly."},
            {"role": "user", "content": text}]
    prompt = tok.apply_chat_template(msgs, tools=tools, add_generation_prompt=True, tokenize=False, enable_thinking=False)
    ids = tok(prompt, return_tensors="pt").to(dev)
    sync(dev); t0 = time.perf_counter()
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=64, do_sample=False)
    sync(dev); dt = time.perf_counter() - t0
    gen = out[0, ids["input_ids"].shape[1]:]
    s = tok.decode(gen, skip_special_tokens=False)
    m = re.search(r'"name"\s*:\s*"([a-z_0-9]+)"', s)
    return (m.group(1) if m and m.group(1) in TOOLS else "none"), dt, int(gen.shape[0])


def one_pass(tok, model, dev, text):
    """Pick the tool from ONE forward pass: score the option letters, no decoding."""
    menu = "\n".join(f"{LETTERS[i]}. {n}: {d}" for i, (n, d) in enumerate(TOOLS.items()))
    msgs = [{"role": "user", "content": f"Message from a heart patient:\n{text}\n\nWhich option fits best?\n{menu}\nAnswer with one letter."}]
    prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, enable_thinking=False)
    ids = tok(prompt, return_tensors="pt").to(dev)
    letter_ids = [tok.encode(c, add_special_tokens=False)[0] for c in LETTERS[:len(TOOLS)]]
    sync(dev); t0 = time.perf_counter()
    with torch.no_grad():
        logits = model(**ids).logits[0, -1]
    choice = int(torch.argmax(logits[letter_ids]))
    sync(dev); dt = time.perf_counter() - t0
    return list(TOOLS)[choice], dt, 1


def cascade(tok, model, dev, text):
    t0 = time.perf_counter()
    if RED_FLAG.search(text):
        return "red_flag", time.perf_counter() - t0, 0
    if MEDICATION.search(text):
        return "none", time.perf_counter() - t0, 0
    tool, _, fp = one_pass(tok, model, dev, text)
    return tool, time.perf_counter() - t0, fp


def embed(tok, model, dev, text):
    """Mean-pooled last hidden state from ONE forward pass (no decoding)."""
    ids = tok(text, return_tensors="pt").to(dev)
    with torch.no_grad():
        h = model(**ids, output_hidden_states=True).hidden_states[-1][0]
    v = h.float().mean(0)
    return v / v.norm()


def make_centroid_router(calib, tok, model, dev):
    """Nearest-centroid over hidden states of a SEPARATE calibration split (symbolic decision on neural features)."""
    by_tool = {}
    for r in calib:
        if r["tool"] == "red_flag":
            continue  # red flags are rules-only, never learned
        by_tool.setdefault(r["tool"], []).append(embed(tok, model, dev, r["text"]))
    names = list(by_tool)
    cents = torch.stack([torch.stack(v).mean(0) for v in by_tool.values()])
    cents = cents / cents.norm(dim=1, keepdim=True)

    def route(tok, model, dev, text):
        t0 = time.perf_counter()
        if RED_FLAG.search(text):
            return "red_flag", time.perf_counter() - t0, 0
        if MEDICATION.search(text):
            return "none", time.perf_counter() - t0, 0
        v = embed(tok, model, dev, text)
        tool = names[int(torch.argmax(cents @ v))]
        sync(dev)
        return tool, time.perf_counter() - t0, 1
    return route


def run(name, fn, rows, tok, model, dev):
    correct, correct_nr, n_nr, times, passes, red_missed = 0, 0, 0, [], [], 0
    for r in rows:
        pred, dt, fp = fn(tok, model, dev, r["text"])
        correct += pred == r["tool"]
        if r["tool"] != "red_flag":
            n_nr += 1
            correct_nr += pred == r["tool"]
        red_missed += r["tool"] == "red_flag" and pred != "red_flag"
        times.append(dt); passes.append(fp)
    n = len(rows)
    return {"config": name, "n": n, "tool_acc": round(correct / n, 3), "tool_acc_excl_red_flag": round(correct_nr / n_nr, 3), "red_flag_missed": red_missed,
            "median_ms": round(statistics.median(times) * 1000, 1), "p95_ms": round(sorted(times)[int(0.95 * (n - 1))] * 1000, 1),
            "mean_forward_passes_or_tokens": round(statistics.mean(passes), 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-0.6B")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    allrows = [json.loads(l) for l in DATA.read_text(encoding="utf-8").splitlines() if l.strip()]
    # Fixed split by id: odd ids = calibration (only config D sees it), even ids = test (every config is scored here).
    calib = [r for r in allrows if int(r["id"][1:]) % 2 == 1]
    rows = [r for r in allrows if int(r["id"][1:]) % 2 == 0]
    rows = rows[: a.limit] if a.limit else rows
    tok, model, dev = load(a.model)
    for _ in range(2):  # warm-up so the first timed call is not a compile
        baseline(tok, model, dev, "hello"); one_pass(tok, model, dev, "hello")
    results = [run("A baseline: LLM writes the tool call", baseline, rows, tok, model, dev),
               run("B one-pass: score option letters, no rules", one_pass, rows, tok, model, dev),
               run("C cascade: red-flag + medication rules, then one-pass", cascade, rows, tok, model, dev),
               run("D cascade: rules, then nearest-centroid on hidden states (calibration split)", make_centroid_router(calib, tok, model, dev), rows, tok, model, dev)]
    meta = {"model": a.model, "device": dev, "dtype": "float32" if dev == "cpu" else "float16", "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else None, "data": str(DATA.relative_to(ROOT)),
            "data_origin": "synthetic", "split": "test = even ids (36 rows); calibration = odd ids (36 rows), used only by config D", "torch": torch.__version__, "date": time.strftime("%Y-%m-%d")}
    out = {"meta": meta, "results": results}
    (ROOT / "experiments" / f"tool_router_demo_results_{a.model.split('/')[-1]}_{dev}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
