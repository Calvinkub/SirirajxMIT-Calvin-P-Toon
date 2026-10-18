// Username-only prototype flow. Clinical context is saved through the API.
(() => {
  const remoteMode = window.HEARTSTEP_API === true;
  const root = document.querySelector('#access-root');
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const steps = ['About you', 'Your records', 'Measurements', 'CPET', 'Review'];
  const units = {heart_rate:'bpm',systolic_bp:'mmHg',diastolic_bp:'mmHg',weight:'kg',height:'cm',spo2:'%',glucose:'mg/dL'};
  const labels = {heart_rate:'Heart rate',systolic_bp:'Systolic blood pressure',diastolic_bp:'Diastolic blood pressure',weight:'Weight',height:'Height',spo2:'Oxygen saturation',glucose:'Blood glucose'};
  let onReady, draft, step=0, busy=false, registrationSaved=false;
  let localUsername='';
  const localProfilesKey='heartstep-local-profiles-v1';
  const blank = username => ({username,patient:{name:'',age:'',sex:'prefer_not_to_say',medicalRecordNumber:'',hospital:'',history:'',allergies:'',goal:'Build a gentle daily routine'},diagnoses:[],medications:[],medicationStatus:'unknown',measurements:[],cpet:null});
  const field = (label,name,value='',attrs='') => `<label class="field">${label}<input name="${name}" value="${esc(value)}" ${attrs}></label>`;
  const area = (label,name,value='',max=1500) => `<label class="field">${label}<textarea name="${name}" maxlength="${max}" rows="3">${esc(value)}</textarea></label>`;
  const localTime = iso => {const date=iso?new Date(iso):new Date();return new Date(date.getTime()-date.getTimezoneOffset()*60000).toISOString().slice(0,16);};
  function savedProfiles() {try{return JSON.parse(localStorage.getItem(localProfilesKey))||{};}catch{return {};}}
  function localState(username,record) {
    if(username==='somchai'&&!record)return {patientId:'demo-somchai',isDemo:true,profile:{name:'Somchai',age:62,diagnosis:'Recovering after MI',goal:'Feel confident walking again',clinicianApproved:true,maxHR:110,rpe:'Easy · able to talk comfortably',allowedActivities:['walking'],source:'Sample clinician-approved CPET plan'},done:[],stopped:false,weeklyWalks:4,activity:{steps:2480,restingHR:68},demoDate:'2026-10-18',record:{patientRecord:null,username:'somchai',dataSource:'fictional_seed',diagnoses:[],medications:[],medicationStatus:'unknown',measurements:[],cpet:null}};
    const diagnosis=record.diagnoses[0]?.name||'Not provided';
    return {patientId:`local-${username}`,isDemo:false,profile:{name:record.patient.name,age:record.patient.age,diagnosis,goal:record.patient.goal,clinicianApproved:false,maxHR:null,rpe:'',allowedActivities:[],source:''},done:[],stopped:false,weeklyWalks:0,activity:null,demoDate:'2026-10-18',record:{patientRecord:record.patient,username,dataSource:'patient_entered',diagnoses:record.diagnoses,medications:record.medications,medicationStatus:record.medicationStatus,measurements:record.measurements,cpet:record.cpet}};
  }
  async function localApi(path,body) {
    const profiles=savedProfiles();
    if(path==='/api/login') {const username=String(body.username).toLowerCase();localUsername=username;return {exists:username==='somchai'||Boolean(profiles[username]),username};}
    if(path==='/api/register') {localUsername=body.username;profiles[localUsername]=body;localStorage.setItem(localProfilesKey,JSON.stringify(profiles));return {patientId:`local-${localUsername}`};}
    if(path==='/api/me') {if(!localUsername)throw Object.assign(new Error('Sign in'),{status:401});return localState(localUsername,profiles[localUsername]);}
    if(path==='/api/logout') {localUsername='';return {ok:true};}
    throw new Error('This action is unavailable in the local demo.');
  }
  async function api(path,body) {
    if(!remoteMode)return localApi(path,body);
    const response=await fetch(path,{method:body===undefined?'GET':'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},...(body===undefined?{}:{body:JSON.stringify(body)}),signal:AbortSignal.timeout(15000)});
    const data=await response.json();
    if(!response.ok){const error=new Error(typeof data.detail==='string'?data.detail:Array.isArray(data.detail)?data.detail.map(e=>`${e.loc.slice(1).join('.')}: ${e.msg}`).join('; '):'Could not save. Please try again.');error.status=response.status;throw error;}
    return data;
  }
  function error(message) {const box=root.querySelector('#access-error');box.textContent=message;box.hidden=false;box.focus();}
  function shell(content, wizard=false) {
    document.body.classList.add('access-mode');root.hidden=false;
    root.innerHTML=`<div class="access-layout ${wizard?'wizard-layout':''}"><aside class="access-story"><a class="brand" href="#"><span class="brand-icon">♡</span> ReVibe<span class="brand-dot">.</span></a><div><span class="eyebrow">YOUR NEXT SMALL STEP</span><h1>A little care.<br>A little confidence.<br>Every day.</h1><p>Your history helps us understand your starting point. Your care team sets the limits.</p></div><small>Siriraj × MIT · Recovery companion prototype<br>Use sample details while testing.</small></aside><section class="access-card">${content}<div id="access-error" class="access-error" role="alert" tabindex="-1" hidden></div></section></div>`;
    root.querySelector('h2')?.focus();
  }
  function login(message='') {
    step=0;draft=null;registrationSaved=false;
    shell(`<span class="eyebrow">WELCOME TO REVIBE</span><h2 tabindex="-1">Let’s start with your username.</h2><p class="access-intro">Already have a profile? We’ll bring you home.<br>New here? We’ll help you set one up.</p><form id="login-form">${field('Username','username','','required minlength="3" maxlength="32" pattern="[A-Za-z0-9_.-]+" autocomplete="username" autocapitalize="none" spellcheck="false" placeholder="e.g. somchai"')}<p class="field-help">3–32 letters, numbers, dots, underscores, or hyphens.</p><button class="button access-primary">Continue <span>↗</span></button></form><p class="review-note">No password is required in this prototype. Try <strong>somchai</strong> for the existing sample patient.</p>`);
    if(message)error(message);
  }
  function diagnosisRow(d={}) {return `<fieldset class="record-row" data-row="diagnosis"><legend>Diagnosis</legend>${field('Diagnosis name','diag_name',d.name,'required maxlength="120" placeholder="As written by your doctor"')}${field('Code (optional)','diag_code',d.code,'maxlength="40" placeholder="e.g. ICD code"')}${field('Diagnosis date (optional)','diag_date',d.diagnosedOn,'type="date"')}${area('Notes (optional)','diag_notes',d.notes,500)}<button type="button" class="text-link" data-remove>Remove diagnosis</button></fieldset>`;}
  function medicationRow(m={}) {return `<fieldset class="record-row" data-row="medication"><legend>Medication</legend>${field('Medication name','med_name',m.name,'required maxlength="120"')}${field('Dose as prescribed (optional)','med_dose',m.dose,'maxlength="80" placeholder="e.g. 5 mg"')}${field('Schedule as prescribed (optional)','med_frequency',m.frequency,'maxlength="120" placeholder="e.g. once daily"')}${area('Notes (optional)','med_notes',m.notes,500)}<button type="button" class="text-link" data-remove>Remove medication</button></fieldset>`;}
  function measurementRow(m={}) {return `<fieldset class="record-row" data-row="measurement"><legend>Measurement</legend><label class="field">Measurement type<select name="measure_kind">${Object.entries(labels).map(([key,label])=>`<option value="${key}" ${key===(m.kind||'heart_rate')?'selected':''}>${label} (${units[key]})</option>`).join('')}</select></label>${field('Value (use the unit shown above)','measure_value',m.value,'required type="number" min="0.01" max="1000" step="any"')}${field('When was it measured?','measure_time',localTime(m.measuredAt),'required type="datetime-local"')}${area('Source or notes (optional)','measure_notes',m.notes,300)}<button type="button" class="text-link" data-remove>Remove measurement</button></fieldset>`;}
  function content() {
    const p=draft.patient;
    if(step===0)return `<h2 tabindex="-1">A little about you.</h2><p class="access-intro">Start with your patient details and what matters to you.</p><div class="form-grid">${field('Name','name',p.name,'required maxlength="80" autocomplete="name"')}${field('Age','age',p.age,'required type="number" min="18" max="110" step="1"')}<label class="field">Sex<select name="sex">${[['prefer_not_to_say','Prefer not to say'],['female','Female'],['male','Male'],['other','Other']].map(([v,l])=>`<option value="${v}" ${p.sex===v?'selected':''}>${l}</option>`).join('')}</select></label>${field('Hospital / clinic (optional)','hospital',p.hospital,'maxlength="120"')}${field('Patient record number (optional)','medicalRecordNumber',p.medicalRecordNumber,'maxlength="80"')}${field('Your recovery goal','goal',p.goal,'required maxlength="250"')}</div>${area('Medical history (optional)','history',p.history)}${area('Allergies (optional; write “none” if known)','allergies',p.allergies,500)}`;
    if(step===1)return `<h2 tabindex="-1">Your records, in your words.</h2><p class="access-intro">Copy details from your care records if you have them. Leave unknown information blank.</p><h3>Diagnoses</h3><div id="diagnosis-rows">${draft.diagnoses.map(diagnosisRow).join('')}</div><button type="button" class="button secondary" data-add="diagnosis">+ Add diagnosis</button><div class="divider"></div><h3>Medications</h3><p class="review-note">Record your existing prescription. This does not change your medication or dose.</p><label class="field">Medication information<select name="medicationStatus">${[['unknown','I’m not sure / I’ll add this later'],['none','I do not currently take medication'],['listed','I have medications to list']].map(([v,l])=>`<option value="${v}" ${draft.medicationStatus===v?'selected':''}>${l}</option>`).join('')}</select></label><div id="medication-rows">${draft.medications.map(medicationRow).join('')}</div><button type="button" class="button secondary" data-add="medication">+ Add medication</button>`;
    if(step===2)return `<h2 tabindex="-1">Your latest measurements.</h2><p class="access-intro">Add readings you already have, such as heart rate, blood pressure, or weight. Include when they were measured.</p><div id="measurement-rows">${draft.measurements.map(measurementRow).join('')}</div><button type="button" class="button secondary" data-add="measurement">+ Add measurement</button><p class="review-note">Don’t have any readings? You can continue without them. A heart-rate reading does not establish an exercise limit.</p>`;
    if(step===3){const c=draft.cpet||{};return `<h2 tabindex="-1">Have a CPET report?</h2><p class="access-intro">If your doctor gave you cardiopulmonary exercise test results, you can record them here. This step is optional.</p><label class="checkbox"><input type="checkbox" name="hasCPET" ${draft.cpet?'checked':''}>I have CPET results from my doctor</label><div id="cpet-fields" ${draft.cpet?'':'hidden'}><div class="form-grid">${field('Test date','testDate',c.testDate,'type="date" data-cpet-required')}${field('Doctor / care team','doctorName',c.doctorName,'maxlength="120" data-cpet-required')}${field('Peak VO₂ (mL/kg/min, optional)','vo2Peak',c.vo2Peak,'type="number" min="0.01" max="150" step="any"')}${field('Heart rate at VT1 (bpm, optional)','heartRateVT1',c.heartRateVT1,'type="number" min="1" max="300" step="any"')}${field('Peak heart rate (bpm, optional)','peakHeartRate',c.peakHeartRate,'type="number" min="1" max="300" step="any"')}</div>${area('Other report results / notes (optional)','reportNotes',c.reportNotes)}</div><p class="review-note">Your report will be saved for review. Exercise stays locked until your care team confirms approved limits.</p>`;}
    return `<h2 tabindex="-1">Ready for your next small step.</h2><p class="access-intro">Review your details before saving your profile.</p><div class="review-summary"><div><span>Username</span><strong>${esc(draft.username)}</strong></div><div><span>Patient</span><strong>${esc(p.name)}, ${esc(p.age)}</strong></div><div><span>Goal</span><strong>${esc(p.goal)}</strong></div><div><span>Diagnoses</span><strong>${draft.diagnoses.length?draft.diagnoses.map(d=>esc(d.name)).join(', '):'Not provided'}</strong></div><div><span>Medications</span><strong>${draft.medications.length?draft.medications.map(m=>esc([m.name,m.dose,m.frequency].filter(Boolean).join(' · '))).join('<br>'):esc(draft.medicationStatus==='none'?'None reported':'Not known / add later')}</strong></div><div><span>Measurements</span><strong>${draft.measurements.length?draft.measurements.map(m=>`${esc(labels[m.kind])}: ${esc(m.value)} ${units[m.kind]}`).join('<br>'):'Not provided'}</strong></div><div><span>CPET</span><strong>${draft.cpet?`Report from ${esc(draft.cpet.doctorName)} · ${esc(draft.cpet.testDate)}`:'Skipped — no report provided'}</strong></div></div><p class="review-note">Your details will be stored for future personalized coaching. Your entered records and CPET report still need clinical verification.</p>`;
  }
  function wizard() {
    shell(`<div class="wizard-top"><span class="eyebrow">YOUR PROFILE · ${esc(draft.username)}</span><button type="button" class="text-link" data-switch>Use another username</button></div><ol class="wizard-progress" aria-label="Profile setup steps">${steps.map((label,i)=>`<li ${i===step?'aria-current="step"':''} class="${i<step?'finished':''}"><span>${i<step?'✓':i+1}</span>${label}</li>`).join('')}</ol><form id="setup-form">${content()}<div class="wizard-actions">${step>0?'<button type="button" class="button ghost" data-back>Back</button>':'<span></span>'}${step===3?'<button type="button" class="text-link" data-skip>Skip CPET</button>':''}<button class="button">${step===4?'Save profile & go home':'Continue'} ↗</button></div></form>`,true);
    toggleCPET();
  }
  function toggleCPET(){const check=root.querySelector('[name="hasCPET"]');if(!check)return;const fields=root.querySelector('#cpet-fields');fields.hidden=!check.checked;fields.querySelectorAll('input,textarea').forEach(el=>{el.disabled=!check.checked;el.required=check.checked&&el.hasAttribute('data-cpet-required');});}
  function collect() {
    const data=new FormData(root.querySelector('#setup-form'));
    const get=n=>String(data.get(n)||'').trim();
    if(step===0){for(const key of Object.keys(draft.patient))draft.patient[key]=get(key);draft.patient.age=Number(draft.patient.age);}
    if(step===1){
      draft.diagnoses=[...root.querySelectorAll('[data-row="diagnosis"]')].map(row=>{const v=n=>row.querySelector(`[name="${n}"]`).value.trim();return {name:v('diag_name'),code:v('diag_code'),diagnosedOn:v('diag_date')||null,notes:v('diag_notes')};});
      draft.medications=[...root.querySelectorAll('[data-row="medication"]')].map(row=>{const v=n=>row.querySelector(`[name="${n}"]`).value.trim();return {name:v('med_name'),dose:v('med_dose'),frequency:v('med_frequency'),notes:v('med_notes')};});
      draft.medicationStatus=draft.medications.length?'listed':get('medicationStatus');
      if(draft.medicationStatus==='listed'&&!draft.medications.length)throw new Error('Add a medication, or select none / not sure.');
    }
    if(step===2)draft.measurements=[...root.querySelectorAll('[data-row="measurement"]')].map(row=>{const v=n=>row.querySelector(`[name="${n}"]`).value;return {kind:v('measure_kind'),value:Number(v('measure_value')),measuredAt:new Date(v('measure_time')).toISOString(),notes:v('measure_notes').trim()};});
    if(step===3){draft.cpet=data.get('hasCPET')?{testDate:get('testDate'),doctorName:get('doctorName'),vo2Peak:get('vo2Peak')?Number(get('vo2Peak')):null,heartRateVT1:get('heartRateVT1')?Number(get('heartRateVT1')):null,peakHeartRate:get('peakHeartRate')?Number(get('peakHeartRate')):null,reportNotes:get('reportNotes')}:null;
      if(draft.cpet&&!draft.cpet.reportNotes&&[draft.cpet.vo2Peak,draft.cpet.heartRateVT1,draft.cpet.peakHeartRate].every(v=>v===null))throw new Error('Enter at least one CPET result or report note, or skip this step.');}
  }
  function finish(data) {root.hidden=true;root.innerHTML='';document.body.classList.remove('access-mode');draft=null;onReady(data);}
  async function openHome(){finish(await api('/api/me'));}
  root.addEventListener('change',e=>{if(e.target.name==='hasCPET')toggleCPET();});
  root.addEventListener('click',e=>{
    const button=e.target.closest('button');if(!button||busy)return;
    if(button.hasAttribute('data-remove'))button.closest('[data-row]').remove();
    if(button.dataset.add){const type=button.dataset.add;const count=root.querySelectorAll(`[data-row="${type}"]`).length;if(count>=(type==='measurement'?50:30)){error('You have reached the maximum number of entries.');return;}root.querySelector(`#${type}-rows`).insertAdjacentHTML('beforeend',({diagnosis:diagnosisRow,medication:medicationRow,measurement:measurementRow}[type])());if(type==='medication')root.querySelector('[name="medicationStatus"]').value='listed';}
    if(button.hasAttribute('data-switch'))login();
    if(button.hasAttribute('data-back')){try{collect();}catch{}step--;wizard();}
    if(button.hasAttribute('data-skip')){draft.cpet=null;step++;wizard();}
  });
  root.addEventListener('submit',async e=>{
    e.preventDefault();if(busy)return;
    const form=e.target;
    try {
      if(form.id==='setup-form'&&step<4){collect();step++;wizard();return;}
      busy=true;form.querySelectorAll('button').forEach(b=>b.disabled=true);
      if(form.id==='login-form'){
        const result=await api('/api/login',{username:new FormData(form).get('username').trim()});
        if(result.exists)await openHome();else {draft=blank(result.username);step=0;wizard();}
      }else if(form.id==='setup-form'){
        if(!registrationSaved){await api('/api/register',draft);registrationSaved=true;}await openHome();
      }
    }catch(err){error(err.message||'Could not connect. Please try again.');}
    finally{busy=false;root.querySelectorAll('button').forEach(b=>b.disabled=false);}
  });
  window.HeartstepAccess={
    async start(callback){onReady=callback;if(!remoteMode){login();return;}shell('<h2 tabindex="-1">Getting things ready…</h2><p class="access-intro">Opening your recovery space.</p>');try{await openHome();}catch(err){login(err.status===401?'':'Could not connect. Check that the server is running and try again.');}},
    async logout(){await api('/api/logout',{});onReady(null);login();},
  };
})();
