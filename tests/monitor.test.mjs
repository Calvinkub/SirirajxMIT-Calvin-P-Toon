import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const ctx = { window: {} };
vm.runInNewContext(await readFile(new URL('../monitor.js', import.meta.url), 'utf8'), ctx);
const M = ctx.window.HeartstepMonitor;
const e = (date, o = {}) => ({ date, sys: 125, dia: 80, hr: 68, weightKg: 78, coffee: false, symptoms: false, ...o });
const TODAY = '2026-10-18';

test('stable week is green', () => {
  const r = M.evaluate(['12', '13', '14', '15', '16', '17', '18'].map(d => e('2026-10-' + d)), TODAY);
  assert.equal(r.zone, 'green');
});
test('weight up 1.2 kg in 2 days is amber; 2.1 kg in 3 days is red', () => {
  const base = ['14', '15', '16'].map(d => e('2026-10-' + d));
  assert.equal(M.evaluate([...base, e('2026-10-17', { weightKg: 79.2 })], '2026-10-17').zone, 'amber');
  assert.equal(M.evaluate([...base, e('2026-10-17', { weightKg: 80.1 })], '2026-10-17').zone, 'red');
});
test('BP and heart-rate red zones', () => {
  assert.equal(M.evaluate([e(TODAY, { sys: 182 })], TODAY).zone, 'red');
  assert.equal(M.evaluate([e(TODAY, { dia: 112 })], TODAY).zone, 'red');
  assert.equal(M.evaluate([e(TODAY, { sys: 85 })], TODAY).zone, 'red');
  assert.equal(M.evaluate([e(TODAY, { hr: 125 })], TODAY).zone, 'red');
  assert.equal(M.evaluate([e(TODAY, { hr: 104 })], TODAY).zone, 'amber');
});
test('coffee adds a recheck note to amber BP but never downgrades red', () => {
  const amber = M.evaluate([e(TODAY, { sys: 165, coffee: true })], TODAY);
  assert.equal(amber.zone, 'amber'); assert.match(amber.reasons[0].text, /recheck in 30 minutes/);
  assert.equal(M.evaluate([e(TODAY, { sys: 185, coffee: true })], TODAY).zone, 'red');
});
test('warning symptom is red, missed diary is amber, empty is amber', () => {
  assert.equal(M.evaluate([e(TODAY, { symptoms: true })], TODAY).zone, 'red');
  assert.equal(M.evaluate([e('2026-10-15')], TODAY).zone, 'amber');
  assert.equal(M.evaluate([], TODAY).zone, 'amber');
});
test('sustained mild BP elevation is amber', () => {
  const r = M.evaluate(['16', '17', '18'].map(d => e('2026-10-' + d, { sys: 144, dia: 88 })), TODAY);
  assert.equal(r.zone, 'amber'); assert.equal(r.reasons[0].code, 'bp-sustained');
});
test('parseEntry rejects impossible values', () => {
  assert.deepEqual([...M.parseEntry({ sys: '300', dia: '80' }, TODAY).errors], ['sys']);
  assert.ok(M.parseEntry({ sys: '80', dia: '120' }, TODAY).errors.includes('bp'));
  assert.equal(M.parseEntry({ sys: '120', dia: '80', hr: '70', weightKg: '78.5', coffee: 'yes' }, TODAY).errors.length, 0);
});
test('seed cohort has green, amber and red patients', () => {
  const zones = M.seedCohort(TODAY).map(p => M.evaluate(p.entries, TODAY).zone);
  for (const z of ['green', 'amber', 'red']) assert.ok(zones.includes(z), z + ' ' + zones);
});
