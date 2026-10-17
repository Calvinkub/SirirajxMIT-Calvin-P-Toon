export const RED_FLAGS = ['chest pain', 'breathlessness', 'dizziness', 'fainting', 'palpitations'];
export function hasRedFlag(text) {
  return /chest\s+(pain|tightness)|breathless|short(ness)?\s+of\s+breath|dizz|faint|palpitation|เจ็บหน้าอก|หายใจไม่ออก|เวียนหัว|เป็นลม|ใจสั่น/i.test(text);
}
export function canExercise(profile, stopped) {
  return !stopped && profile.clinicianApproved === true && Number.isFinite(profile.maxHR) && profile.maxHR > 0 && profile.allowedActivities.includes('walking') && Boolean(profile.rpe);
}
