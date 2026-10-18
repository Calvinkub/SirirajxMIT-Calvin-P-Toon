// Remote monitoring rules: patient diary (BP, weight, heart rate, coffee) -> zone (green / amber / red).
// Plain rules, no model. Thresholds are defaults for a prototype; a clinician sets them per patient.
// Works in the browser (window.HeartstepMonitor) and under node (vm / require).
(function (root) {
  const THRESHOLDS = {
    weight: { amber: { kg: 1.0, days: 2 }, amberWeek: { kg: 1.5, days: 7 }, red: { kg: 2.0, days: 3 }, redWeek: { kg: 2.5, days: 7 } },
    bp: { redSys: 180, redDia: 110, lowSys: 90, amberSys: 160, amberDia: 100, softLowSys: 100, sustained: { sys: 140, dia: 90, readings: 3 } },
    hr: { redHigh: 120, redLow: 45, amberHigh: 100, amberLow: 50 },
    missedDays: 2,
  };
  const RANK = { green: 0, amber: 1, red: 2 };
  const DAY = 86400000;
  const day = d => Math.floor(Date.parse(d + 'T00:00:00Z') / DAY);
  const isNum = v => typeof v === 'number' && Number.isFinite(v);
  const sortEntries = entries => [...entries].sort((a, b) => a.date.localeCompare(b.date));

  function evaluate(entries, today, limits) {
    const T = { ...THRESHOLDS, ...(limits || {}) };
    const list = sortEntries(entries || []);
    const reasons = [];
    const add = (zone, code, text) => reasons.push({ zone, code, text });
    const last = list[list.length - 1];
    if (!last) return { zone: 'amber', reasons: [{ zone: 'amber', code: 'no-data', text: 'No diary entries yet.' }], action: actionFor('amber'), last: null };
    const gap = day(today) - day(last.date);
    if (gap >= T.missedDays) add('amber', 'missed', `No diary for ${gap} days.`);
    if (last.symptoms) add('red', 'symptoms', 'Patient reported a warning symptom (chest pain, breathlessness or dizziness).');

    if (isNum(last.weightKg)) {
      const gainSince = n => {
        const base = list.filter(e => isNum(e.weightKg) && day(last.date) - day(e.date) > 0 && day(last.date) - day(e.date) <= n);
        if (!base.length) return null;
        return +(last.weightKg - Math.min(...base.map(e => e.weightKg))).toFixed(1);
      };
      const g3 = gainSince(T.weight.red.days), g7 = gainSince(7), g2 = gainSince(T.weight.amber.days);
      if (g3 !== null && g3 >= T.weight.red.kg) add('red', 'weight', `Weight up ${g3} kg in ${T.weight.red.days} days.`);
      else if (g7 !== null && g7 >= T.weight.redWeek.kg) add('red', 'weight', `Weight up ${g7} kg in 7 days.`);
      else if (g2 !== null && g2 >= T.weight.amber.kg) add('amber', 'weight', `Weight up ${g2} kg in ${T.weight.amber.days} days.`);
      else if (g7 !== null && g7 >= T.weight.amberWeek.kg) add('amber', 'weight', `Weight up ${g7} kg in 7 days.`);
    }

    if (isNum(last.sys) && isNum(last.dia)) {
      const b = T.bp, tag = last.coffee ? ' Coffee today: recheck in 30 minutes.' : '';
      if (last.sys >= b.redSys || last.dia >= b.redDia) add('red', 'bp', `BP ${last.sys}/${last.dia} is in the red zone.`);
      else if (last.sys < b.lowSys) add('red', 'bp', `BP ${last.sys}/${last.dia} is very low.`);
      else if (last.sys >= b.amberSys || last.dia >= b.amberDia) add('amber', 'bp', `BP ${last.sys}/${last.dia} is high.${tag}`);
      else if (last.sys < b.softLowSys) add('amber', 'bp', `BP ${last.sys}/${last.dia} is low.`);
      else {
        const s = b.sustained, tail = list.slice(-s.readings);
        if (tail.length === s.readings && tail.every(e => isNum(e.sys) && (e.sys >= s.sys || e.dia >= s.dia))) add('amber', 'bp-sustained', `BP at or above ${s.sys}/${s.dia} for ${s.readings} readings in a row.`);
      }
    }

    if (isNum(last.hr)) {
      const h = T.hr, tag = last.coffee ? ' Coffee today: recheck in 30 minutes.' : '';
      if (last.hr > h.redHigh || last.hr < h.redLow) add('red', 'hr', `Resting heart rate ${last.hr} is in the red zone.`);
      else if (last.hr > h.amberHigh) add('amber', 'hr', `Resting heart rate ${last.hr} is high.${tag}`);
      else if (last.hr < h.amberLow) add('amber', 'hr', `Resting heart rate ${last.hr} is low.`);
    }

    const zone = reasons.reduce((z, r) => (RANK[r.zone] > RANK[z] ? r.zone : z), 'green');
    return { zone, reasons, action: actionFor(zone, last.symptoms), last };
  }

  function actionFor(zone, symptoms) {
    if (zone === 'red') return symptoms ? 'Call the patient now. If symptoms continue, advise 1669.' : 'Nurse calls the patient today. Doctor reviews if not resolved.';
    if (zone === 'amber') return 'Nurse check-in within 48 hours. Coach sends a nudge.';
    return 'No action. Keep the routine.';
  }

  // Deterministic synthetic cohort for the dashboard. Everything here is invented.
  function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const iso = n => new Date(n * DAY).toISOString().slice(0, 10);
  function series(today, spec, seed) {
    const r = rng(seed), n = day(today), out = [];
    for (let i = 13; i >= 0; i--) {
      if (spec.skipLast && i < spec.skipLast) continue;
      const k = 13 - i, drift = spec.weightDrift ? spec.weightDrift(k) : 0;
      out.push({
        date: iso(n - i), sys: Math.round(spec.sys + (spec.sysDrift ? spec.sysDrift(k) : 0) + (r() - 0.5) * 8), dia: Math.round(spec.dia + (spec.diaDrift ? spec.diaDrift(k) : 0) + (r() - 0.5) * 5),
        hr: Math.round(spec.hr + (spec.hrDrift ? spec.hrDrift(k) : 0) + (r() - 0.5) * 6), weightKg: +(spec.weight + drift + (r() - 0.5) * 0.3).toFixed(1),
        coffee: spec.coffee ? k === 13 || r() < 0.5 : r() < 0.3, symptoms: Boolean(spec.symptomLast && k === 13), prom: 3 + Math.round(r()), prem: 4 + Math.round(r() - 0.4),
      });
    }
    return out;
  }
  function seedCohort(today) {
    const P = [
      ['cmc-p01', 'Somchai K.', 62, 'MI this year, hypertension', { sys: 128, dia: 80, hr: 68, weight: 78, weightDrift: k => (k > 8 ? 0.35 * (k - 8) : 0) }],
      ['cmc-p02', 'Prani T.', 71, 'Hypertension, low tech comfort', { sys: 148, dia: 92, hr: 74, weight: 62 }],
      ['cmc-p03', 'Wichai S.', 66, 'Heart failure, LVEF 42%', { sys: 118, dia: 74, hr: 82, weight: 84, weightDrift: k => (k > 9 ? 0.7 * (k - 9) : 0) }],
      ['cmc-p04', 'Anan P.', 59, 'LVEF 30%, ICD', { sys: 110, dia: 70, hr: 78, weight: 90, skipLast: 3 }],
      ['cmc-p05', 'Malee R.', 64, '6 weeks after bypass', { sys: 124, dia: 78, hr: 70, weight: 58 }],
      ['cmc-p07', 'Boonmee C.', 67, 'Chest tightness reported', { sys: 150, dia: 94, hr: 96, weight: 73, symptomLast: true }],
      ['cmc-p08', 'Lamai N.', 69, 'AF, several conditions', { sys: 136, dia: 86, hr: 108, weight: 66, coffee: true }],
    ];
    return P.map(([id, name, age, dx, spec], i) => ({ id, name, age, dx, entries: series(today, spec, 42 + i) }));
  }

  const STORE_KEY = 'heartstep-diary-v1';
  function loadDiary(storage) { try { const v = JSON.parse(storage.getItem(STORE_KEY)); return Array.isArray(v) ? v : []; } catch { return []; } }
  function saveEntry(storage, entry) {
    const list = loadDiary(storage).filter(e => e.date !== entry.date);
    list.push(entry);
    const out = sortEntries(list).slice(-60);
    try { storage.setItem(STORE_KEY, JSON.stringify(out)); } catch { /* storage may be blocked */ }
    return out;
  }
  function parseEntry(fields, date) {
    const num = k => { const v = String(fields[k] ?? '').trim(); return v === '' ? null : Number(v); };
    const e = { date, sys: num('sys'), dia: num('dia'), hr: num('hr'), weightKg: num('weightKg'), coffee: fields.coffee === 'yes', symptoms: fields.symptoms === 'yes', prom: num('prom'), prem: num('prem') };
    const bad = [['sys', 60, 260], ['dia', 30, 160], ['hr', 25, 220], ['weightKg', 20, 300], ['prom', 1, 5], ['prem', 1, 5]].filter(([k, lo, hi]) => e[k] !== null && !(e[k] >= lo && e[k] <= hi)).map(([k]) => k);
    if ((e.sys === null) !== (e.dia === null)) bad.push('bp');
    if (e.sys !== null && e.dia !== null && e.sys <= e.dia) bad.push('bp');
    return { entry: e, errors: bad };
  }

  const api = { THRESHOLDS, evaluate, seedCohort, loadDiary, saveEntry, parseEntry, STORE_KEY, day, iso };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.HeartstepMonitor = api;
})(typeof window !== 'undefined' ? window : globalThis);
