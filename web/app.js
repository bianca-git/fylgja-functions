// Fylgja Web UI - Minimal Frontend Logic
// NOTE: Backend endpoints must be implemented for full functionality

const API_BASE = '/api'; // Adjust if deploying under a different path

// DOM Elements
const checkinForm = document.getElementById('checkin-form');
const checkinInput = document.getElementById('checkin-input');
const tasksList = document.getElementById('tasks-list');
const summaryContent = document.getElementById('summary-content');

// Fetch and render tasks
async function loadTasks() {
  const res = await fetch(`${API_BASE}/tasks`);
  const data = await res.json();
  tasksList.innerHTML = '';
  data.tasks.forEach(task => {
    const li = document.createElement('li');
    li.textContent = task.taskDescription;
    if (task.status === 'Done') li.classList.add('done');
    // Actions
    const actions = document.createElement('span');
    actions.className = 'task-actions';
    if (task.status !== 'Done') {
      const doneBtn = document.createElement('button');
      doneBtn.textContent = 'Mark Done';
      doneBtn.onclick = () => markTaskDone(task.id);
      actions.appendChild(doneBtn);
    }
    li.appendChild(actions);
    tasksList.appendChild(li);
  });
}

// Submit check-in
checkinForm.onsubmit = async (e) => {
  e.preventDefault();
  const text = checkinInput.value.trim();
  if (!text) return;
  await fetch(`${API_BASE}/checkin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  checkinInput.value = '';
  loadTasks();
  loadSummary();
};

// Mark task as done
async function markTaskDone(id) {
  await fetch(`${API_BASE}/tasks/${id}/done`, { method: 'POST' });
  loadTasks();
  loadSummary();
}

// Fetch and render summary
async function loadSummary() {
  const res = await fetch(`${API_BASE}/summary`);
  const data = await res.json();
  summaryContent.textContent = data.summary || 'No summary yet.';
}

// Initial load
loadTasks();
loadSummary();
