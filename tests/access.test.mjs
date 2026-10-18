import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { JSDOM } from 'jsdom';
import { canExercise, hasRedFlag, RED_FLAGS } from '../safety.js';

const [html, accessSource, appSource] = await Promise.all(['index.html','access.js','app.js'].map(f=>readFile(new URL('../'+f,import.meta.url),'utf8')));
const settle=async()=>{for(let i=0;i<4;i++)await new Promise(r=>setImmediate(r));};
function record(body) {
  return {patientRecord:body?.patient||null,username:body?.username||'somchai',dataSource:body?'patient_entered':'fictional_seed',diagnoses:body?.diagnoses||[],medications:body?.medications||[],medicationStatus:body?.medicationStatus||'unknown',measurements:(body?.measurements||[]).map(m=>({...m,unit:'bpm'})),cpet:body?.cpet||null};
}
function state(body) {
  return {patientId:body?'patient-test':'demo-somchai',isDemo:!body,profile:body?{...body.patient,diagnosis:body.diagnoses[0]?.name||'Not provided',clinicianApproved:false,maxHR:null,rpe:'',allowedActivities:[],source:''}:{name:'Somchai',age:62,goal:'Feel confident walking again',diagnosis:'Recovering after MI',clinicianApproved:true,maxHR:110,rpe:'Easy',allowedActivities:['walking'],source:'Sample'},done:[],stopped:false,weeklyWalks:body?0:4,activity:body?null:{steps:2480,restingHR:68},demoDate:'2026-10-18',record:record(body)};
}
async function boot({offline=false}={}) {
  const dom=new JSDOM(html,{url:'http://127.0.0.1:8000/',runScripts:'outside-only'});
  const {window}=dom;let active=null,registered=null;
  window.HTMLDialogElement.prototype.close=function(){this.open=false;};
  window.HTMLDialogElement.prototype.showModal=function(){this.open=true;};
  Object.assign(window,{HEARTSTEP_API:true,canExercise,hasRedFlag,RED_FLAGS,AbortSignal});
  window.fetch=async(path,options={})=>{
    if(offline)throw new Error('offline');
    const body=options.body?JSON.parse(options.body):null;
    let value,status=200;
    if(path==='/api/me'){value=active||{detail:'Sign in'};status=active?200:401;}
    else if(path==='/api/login'){active=body.username==='somchai'?state():null;value={exists:!!active,username:body.username.toLowerCase()};}
    else if(path==='/api/register'){registered=body;active=state(body);value={patientId:active.patientId};status=201;}
    else if(path==='/api/logout'){active=null;value={ok:true};}
    else throw new Error('Unexpected API '+path);
    return {ok:status<400,status,json:async()=>value};
  };
  window.eval(accessSource);
  window.eval(appSource.replace(/^import .*?;\n/,''));
  await settle();
  const q=selector=>window.document.querySelector(selector);
  return {window,q,dom,registered:()=>registered,async submit(id){const form=q('#'+id);assert.ok(form.checkValidity(),id+' must be valid');form.requestSubmit();await settle();},async click(selector){q(selector).click();await settle();},set(name,value){q(`[name="${name}"]`).value=value;}};
}

test('existing username opens its home, sign out returns to username screen',async()=>{
  const app=await boot();
  try {
    assert.match(app.q('#access-root').textContent,/Let’s start with your username/);
    app.set('username','somchai');await app.submit('login-form');
    assert.equal(app.q('#access-root').hidden,true);
    assert.match(app.q('main').textContent,/Good morning, Somchai/);
    assert.equal(app.q('#patient-name').textContent,'Somchai');
    await app.click('#logout-button');
    assert.equal(app.q('#access-root').hidden,false);
    assert.ok(app.window.document.body.classList.contains('access-mode'));
  }finally{app.dom.window.close();}
});

test('new username completes records and measurements, skips CPET, and reaches its own home',async()=>{
  const app=await boot();
  try {
    app.set('username','new-patient');await app.submit('login-form');
    app.set('name','<Test Patient>');app.set('age','60');app.set('hospital','Sample Hospital');app.set('history','Fictional prior history');
    await app.submit('setup-form');
    await app.click('[data-add="diagnosis"]');app.set('diag_name','Sample diagnosis');
    await app.click('[data-add="medication"]');app.set('med_name','Fictional medicine');app.set('med_dose','As prescribed');
    await app.submit('setup-form');
    await app.click('[data-add="measurement"]');app.set('measure_value','68');
    await app.submit('setup-form');
    assert.equal(app.q('#cpet-fields').hidden,true);
    await app.click('[data-skip]');
    assert.match(app.q('#access-root').textContent,/Skipped — no report provided/);
    await app.click('[data-back]');
    await app.click('[data-skip]');await app.submit('setup-form');
    const saved=app.registered();
    assert.equal(saved.cpet,null);assert.equal(saved.patient.history,'Fictional prior history');
    assert.equal(saved.medications[0].name,'Fictional medicine');
    assert.equal(saved.measurements[0].value,68);assert.ok(saved.measurements[0].measuredAt.endsWith('Z'));
    assert.equal(app.q('#access-root').hidden,true);
    assert.match(app.q('main').textContent,/Profile/);
    assert.match(app.q('main').textContent,/Link your Info/);
    assert.match(app.q('main').textContent,/Clinical summary/);
    assert.match(app.q('main').textContent,/My Goal/);
    assert.match(app.q('main').textContent,/<Test Patient>/);
    assert.doesNotMatch(app.q('main').textContent,/2,480|Good afternoon, Somchai/);
    await app.click('[data-page="profile"]');app.window.dispatchEvent(new app.window.HashChangeEvent('hashchange'));
    assert.match(app.q('main').textContent,/Fictional medicine/);
    assert.match(app.q('main').textContent,/No CPET report provided/);
    assert.equal(app.q('main test'),null);
  }finally{app.dom.window.close();}
});

test('CPET inputs become required only when selected and retain results on back navigation',async()=>{
  const app=await boot();
  try {
    app.set('username','cpet-patient');await app.submit('login-form');app.set('name','CPET Test');app.set('age','58');
    await app.submit('setup-form');await app.submit('setup-form');await app.submit('setup-form');
    const check=app.q('[name="hasCPET"]');check.checked=true;check.dispatchEvent(new app.window.Event('change',{bubbles:true}));
    assert.equal(app.q('#cpet-fields').hidden,false);
    assert.equal(app.q('#setup-form').checkValidity(),false);
    app.set('testDate','2026-10-17');app.set('doctorName','Fictional Doctor');app.set('heartRateVT1','100');
    await app.submit('setup-form');await app.click('[data-back]');
    assert.equal(app.q('[name="heartRateVT1"]').value,'100');
    await app.submit('setup-form');await app.submit('setup-form');
    assert.equal(app.registered().cpet.heartRateVT1,100);
    assert.match(app.q('main').textContent,/Exercise missions stay locked/);
  }finally{app.dom.window.close();}
});

test('unavailable server keeps login visible and never opens sample patient data',async()=>{
  const app=await boot({offline:true});
  try{assert.ok(app.window.document.body.classList.contains('access-mode'));assert.match(app.q('#access-error').textContent,/Could not connect/);assert.equal(app.q('#access-root').hidden,false);}
  finally{app.dom.window.close();}
});
