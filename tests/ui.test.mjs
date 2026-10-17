import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { canExercise, hasRedFlag, RED_FLAGS } from '../safety.js';

const source = (await readFile(new URL('../app.js', import.meta.url),'utf8')).replace(/^import .*?;\n/,'');
function boot() {
  const listeners = {}, nodes = {}, saved = {};
  function node(selector) { return nodes[selector] ||= {innerHTML:'',textContent:'',open:false,classList:{add(){},remove(){}},focus(){},scrollTo(){},addEventListener(type,fn){listeners[`${selector}:${type}`]=fn;},showModal(){this.open=true;},close(){this.open=false;}}; }
  const context = {canExercise,hasRedFlag,RED_FLAGS,console,location:{hash:'#today'},localStorage:{getItem:k=>saved[k]||null,setItem:(k,v)=>saved[k]=v},document:{querySelector:node,addEventListener:(event,fn)=>listeners[event]=fn},window:{addEventListener:(event,fn)=>listeners[event]=fn},setTimeout:()=>0,clearTimeout(){},FormData:class{constructor(form){this.fields=form.fields;}get(key){return this.fields[key];}}};
  vm.runInNewContext(source,context);
  return { nodes, saved, page(name){context.location.hash=`#${name}`;listeners.hashchange();},click(action,extra={}){const target={dataset:{action,...extra}};listeners.click({target:{closest:()=>target}});},submit(id,fields){listeners.submit({preventDefault(){},target:{id,fields}});},html:()=>node('main').innerHTML,modal:()=>node('#modal-content').innerHTML,state:()=>JSON.parse(saved['heartstep-demo-v1'])};
}
test('all five screens render and mission completion persists',()=>{
  const app=boot();
  assert.match(app.html(),/Your two little missions/);
  app.click('walk');assert.match(app.modal(),/I’ve finished my walk/);
  app.click('finish-walk');assert.deepEqual(app.state().done,['walk']);
  app.click('medication');assert.deepEqual(app.state().done,['walk','medication']);
  app.click('undo',{kind:'walk'});assert.deepEqual(app.state().done,['medication']);
  for(const [page,text] of [['plan','Your week, one step'],['coach','You’ve got someone'],['community','A little easier'],['profile','Your recovery profile']]){app.page(page);assert.ok(app.html().includes(text),page);}
});
test('onboarding without clinician limits locks exercise and escapes patient input',()=>{
  const app=boot();app.submit('onboarding-form',{name:'<img src=x>',age:'60',diagnosis:'Recovering after MI',goal:'Build a gentle daily routine'});
  app.page('today');assert.match(app.html(),/Waiting for clinician-approved limits/);assert.match(app.html(),/data-action="walk"[^>]*disabled/);
  assert.match(app.html(),/&lt;img src=x&gt;/);assert.doesNotMatch(app.html(),/<img src=x>/);
  app.click('walk');assert.equal(app.nodes['#modal'].open,false);assert.equal(app.state().profile.clinicianApproved,false);
});
test('warning symptom in chat immediately pauses exercise and further coaching',()=>{
  const app=boot();app.page('coach');app.submit('chat-form',{message:'I have chest pain'});
  assert.equal(app.state().stopped,true);assert.match(app.html(),/Stop now and call 1669/);
  const count=app.state().messages.length;app.submit('chat-form',{message:'Can I continue?'});assert.equal(app.state().messages.length,count);
  app.page('today');assert.match(app.html(),/data-action="walk"[^>]*disabled/);
});
test('symptom picker stops an active walk and reset restores sample state',()=>{
  const app=boot();app.click('walk');app.click('red-flag');app.click('finish-walk');assert.deepEqual(app.state().done,[]);
  app.click('confirm-reset');assert.equal(app.state().stopped,false);assert.equal(app.state().profile.clinicianApproved,true);
});
