import { test } from 'node:test';
import assert from 'node:assert/strict';
import { hasRedFlag, canExercise } from '../safety.js';
const approved={clinicianApproved:true,maxHR:110,rpe:'Easy talk test',allowedActivities:['walking']};
test('warning symptoms override coaching in English and Thai',()=>{
  for(const text of ['I have chest pain','I feel dizzy','unusual breathlessness','shortness of breath','I was fainting','palpitations','เจ็บหน้าอก','หายใจไม่ออก','เวียนหัว','เป็นลม','ใจสั่น'])assert.equal(hasRedFlag(text),true,text);
  assert.equal(hasRedFlag('Help me build a routine'),false);
});
test('exercise requires clinician limits, allowed activity, and effort guidance',()=>{
  assert.equal(canExercise(approved,false),true);
  for(const profile of [{...approved,clinicianApproved:false},{...approved,maxHR:null},{...approved,maxHR:0},{...approved,allowedActivities:[]},{...approved,rpe:''}])assert.equal(canExercise(profile,false),false);
  assert.equal(canExercise(approved,true),false);
});
