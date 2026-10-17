// Runs against the local fictional demo and resets today's sample progress.
import assert from 'node:assert/strict';
const base=process.env.HEARTSTEP_URL || 'http://127.0.0.1:8000';
async function request(path,method='GET',body,status=200) {
  const response=await fetch(base+path,{method,headers:{'Content-Type':'application/json'},
    ...(body===undefined?{}:{body:JSON.stringify(body)}),signal:AbortSignal.timeout(15000)});
  assert.equal(response.status,status,`${method} ${path}: ${await response.clone().text()}`);
  return response.json();
}
assert.equal((await request('/api/health')).database,'iris');
await request('/api/demo/reset','POST');
try {
  const initial=await request('/api/demo');
  assert.equal(initial.profile.fhirPatientId,'demo-somchai');
  assert.equal(initial.profile.maxHR,110);
  assert.equal(initial.activity.steps,2480);
  assert.equal(initial.weeklyWalks,4);
  const completed=await request('/api/demo/completions/walk','PUT',{completed:true});
  assert.ok(completed.done.includes('walk'));
  assert.equal(completed.weeklyWalks,5);
  // A repeated write must remain idempotent.
  await request('/api/demo/completions/walk','PUT',{completed:true});
  assert.equal((await request('/api/demo')).weeklyWalks,5);
  await request('/api/demo/completions/walk','PUT',{completed:false});
  await request('/api/demo/stop','POST');
  assert.equal((await request('/api/demo')).stopped,true);
  await request('/api/demo/completions/walk','PUT',{completed:true},409);
  await request('/api/demo/completions/medication','PUT',{completed:true});
  await request('/api/demo/completions/walk','PUT',{completed:true,maxHR:200},422);
  console.log('IRIS smoke passed: real reads/writes, idempotency, symptom stop, and clinical-field rejection.');
} finally {
  await request('/api/demo/reset','POST');
}
