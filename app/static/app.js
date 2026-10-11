const form = document.querySelector('#mission-form');
const submitBtn = document.querySelector('#submit-btn');
const emptyState = document.querySelector('#empty-state');
const loadingState = document.querySelector('#loading-state');
const missionCard = document.querySelector('#mission-card');
const errorState = document.querySelector('#error-state');
const completionMessage = document.querySelector('#completion-message');
let missionCount = 0;
let lastMission = null;

function showState(state) {
  [emptyState, loadingState, missionCard, errorState].forEach(el => el.classList.add('hidden'));
  state.classList.remove('hidden');
}
function getFormData() {
  return Object.fromEntries(new FormData(form).entries());
}
async function generateMission() {
  showState(loadingState);
  submitBtn.disabled = true;
  submitBtn.querySelector('span:first-child').textContent = 'Creating your mission…';
  completionMessage.classList.add('hidden');
  try {
    const response = await fetch('/api/mission', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(getFormData())
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Something went wrong. Please try again.');
    lastMission = data;
    missionCount += 1;
    document.querySelector('#mission-num').textContent = String(missionCount).padStart(2, '0');
    document.querySelector('#mission-time').textContent = `${data.estimated_minutes} MIN`;
    document.querySelector('#mission-title').textContent = data.title;
    document.querySelector('#mission-why').textContent = data.why;
    document.querySelector('#mission-mindful').textContent = data.mindful_prompt;
    document.querySelector('#mission-safety').textContent = data.safety_note ? `A SMALL SAFETY NOTE · ${data.safety_note}` : '';
    const list = document.querySelector('#mission-checklist');
    list.replaceChildren();
    data.checklist.forEach(step => { const li = document.createElement('li'); li.textContent = step; list.appendChild(li); });
    showState(missionCard);
    // Keep a small local-only history; no network call is made for storage.
    const history = JSON.parse(localStorage.getItem('touchgrass-history') || '[]');
    history.unshift({title: data.title, at: new Date().toISOString()});
    localStorage.setItem('touchgrass-history', JSON.stringify(history.slice(0, 10)));
  } catch (error) {
    document.querySelector('#error-message').textContent = error.message;
    showState(errorState);
  } finally {
    submitBtn.disabled = false;
    submitBtn.querySelector('span:first-child').textContent = 'Make me a mission';
  }
}
form.addEventListener('submit', event => { event.preventDefault(); generateMission(); });
document.querySelector('#another-btn').addEventListener('click', generateMission);
document.querySelector('#retry-btn').addEventListener('click', generateMission);
document.querySelector('#complete-btn').addEventListener('click', () => {
  completionMessage.classList.remove('hidden');
  document.querySelector('#complete-btn').textContent = 'Mission accepted ✓';
  document.querySelector('#complete-btn').disabled = true;
});
if ('serviceWorker' in navigator) window.addEventListener('load', () => navigator.serviceWorker.register('/static/sw.js').catch(() => {}));
