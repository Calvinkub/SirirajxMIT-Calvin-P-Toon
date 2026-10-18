import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { canExercise, hasRedFlag, RED_FLAGS } from '../safety.js';

const source = (await readFile(new URL('../app.js', import.meta.url),'utf8')).replace(/^import .*?;\n/,'');
function boot(options={}) {
  const listeners = {}, nodes = {}, saved = {};
  function node(selector) { return nodes[selector] ||= {innerHTML:'',textContent:'',open:false,classList:{add(){},remove(){}},focus(){},scrollTo(){},addEventListener(type,fn){listeners[`${selector}:${type}`]=fn;},showModal(){this.open=true;},close(){this.open=false;}}; }
  const context = {canExercise,hasRedFlag,RED_FLAGS,console,location:{hash:'#today'},localStorage:{getItem:k=>saved[k]||null,setItem:(k,v)=>saved[k]=v},document:{querySelector:node,addEventListener:(event,fn)=>listeners[event]=fn},fetch:options.fetch,AbortSignal,window:{HEARTSTEP_API:options.iris === true,addEventListener:(event,fn)=>listeners[event]=fn},setTimeout:()=>0,clearTimeout(){},FormData:class{constructor(form){this.fields=form.fields;}get(key){return this.fields[key];}}};
  vm.runInNewContext(source,context);
  return { nodes, saved, page(name){context.location.hash=`#${name}`;listeners.hashchange();},click(action,extra={}){const target={dataset:{action,...extra}};listeners.click({target:{closest:()=>target}});},submit(id,fields){listeners.submit({preventDefault(){},target:{id,fields}});},html:()=>node('main').innerHTML,modal:()=>node('#modal-content').innerHTML,state:()=>JSON.parse(saved['heartstep-demo-v1'])};
}
test('all five screens render and mission completion persists',()=>{
  const app=boot();
  assert.equal(app.nodes['#agent-observer'].hidden,true);
  assert.match(app.html(),/class="sample-badge synced"><i aria-hidden="true"><\/i>Synced/);
  assert.doesNotMatch(app.html(),/>Sample data<\/span>/);
  assert.match(app.html(),/Today’s session/);
  app.click('walk');assert.match(app.modal(),/I’ve finished my walk/);
  app.click('finish-walk');assert.deepEqual(app.state().done,['walk']);
  app.click('medication');assert.deepEqual(app.state().done,['walk','medication']);
  app.click('undo',{kind:'walk'});assert.deepEqual(app.state().done,['medication']);
  for(const [page,text] of [['plan','Workout Task Checklist'],['coach','You’ve got someone'],['community','A little easier'],['profile','Clinical summary']]){app.page(page);assert.ok(app.html().includes(text),page);}
});
test('onboarding without clinician limits locks exercise and escapes patient input',()=>{
  const app=boot();app.submit('onboarding-form',{name:'<img src=x>',age:'60',diagnosis:'Recovering after MI',goal:'Build a gentle daily routine'});
  app.page('today');assert.match(app.html(),/Start Session/);assert.match(app.html(),/data-action="walk"[^>]*disabled/);
  assert.match(app.html(),/&lt;img src=x&gt;/);assert.doesNotMatch(app.html(),/<img src=x>/);
  app.click('walk');assert.equal(app.nodes['#modal'].open,false);assert.equal(app.state().profile.clinicianApproved,false);
});
test('warning symptom in chat immediately pauses exercise and further coaching',()=>{
  const app=boot();app.page('coach');app.submit('chat-form',{message:'I have chest pain'});
  assert.equal(app.state().stopped,true);assert.match(app.html(),/Stop now and call 1669/);
  const count=app.state().messages.length;app.submit('chat-form',{message:'Can I continue?'});assert.equal(app.state().messages.length,count);
  app.page('today');assert.match(app.html(),/data-action="walk"[^>]*disabled/);
});
test('agent-flow chat offers activities, frequency, and a seven-day plan',()=>{
  const app=boot();app.page('coach');app.submit('chat-form',{message:'I used to play tennis. Maybe badminton or bowling?'});
  assert.match(app.html(),/Social badminton/);assert.match(app.html(),/Seniors(?:'|&#39;) bowling league/);
  app.click('chat-option',{index:'0'});assert.match(app.html(),/Start gently: 2 sessions/);
  app.click('chat-frequency',{count:'2'});assert.match(app.html(),/This week · heart rate under 110/);
  assert.equal((app.html().match(/<div><b>/g)||[]).length,7);
  assert.doesNotMatch(app.html(),/What the AI is doing/);
  assert.equal(app.nodes['#agent-observer'].hidden,false);
  assert.match(app.nodes['#agent-observer-frame'].src,/agent-flow-demo\.html\?prompt=I%20used%20to%20play%20tennis/);
});
test('symptom picker stops an active walk and reset restores sample state',()=>{
  const app=boot();app.click('walk');app.click('red-flag');app.click('finish-walk');assert.deepEqual(app.state().done,[]);
  app.click('confirm-reset');assert.equal(app.state().stopped,false);assert.equal(app.state().profile.clinicianApproved,true);
});

const settled=()=>new Promise(resolve=>setImmediate(resolve));
const snapshot={profile:{name:'Somchai',age:62,diagnosis:'Recovering after MI',goal:'Feel confident walking again',clinicianApproved:true,maxHR:110,rpe:'Easy',allowedActivities:['walking'],source:'Fictional plan'},done:[],stopped:false,weeklyWalks:4,activity:{steps:2480,restingHR:68}};
test('IRIS mode loads database profile and waits for a successful completion write',async()=>{
  const calls=[]; let finish;
  const app=boot({iris:true,fetch:async(path,options)=>{
    calls.push({path,options});
    if(options.method==='PUT')return new Promise(resolve=>{finish=()=>resolve({ok:true,json:async()=>({...snapshot,done:['walk'],weeklyWalks:5})});});
    return {ok:true,json:async()=>snapshot};
  }});
  await settled();
  assert.match(app.html(),/Limit 110/);
  app.click('walk');app.click('finish-walk');
  assert.doesNotMatch(app.html(),/✓ Completed/);
  finish();await settled();
  assert.match(app.html(),/10\/20/);
  assert.equal(calls[1].path,'/api/me/completions/walk');
  assert.equal(JSON.parse(calls[1].options.body).completed,true);
});
test('IRIS connection failure locks exercise and reports unavailable storage',async()=>{
  const app=boot({iris:true,fetch:async()=>{throw new Error('offline');}});
  await settled();
  assert.match(app.html(),/data-action="walk"[^>]*disabled/);
  assert.equal(app.nodes['.demo-pill'].textContent,'IRIS unavailable');
  app.click('medication');assert.doesNotMatch(app.html(),/✓ Completed/);
});
