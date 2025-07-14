// Fylgja Web UI - Handles check-in, tasks, and summary interactions
const API_BASE = "https://us-central1-fyl-gja.cloudfunctions.net"

// --- Check-in Submission ---
document.getElementById("checkin-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("checkin-text").value.trim();
  if (!text) return;
  setLoading("checkin-response", true);
  try {
    const res = await fetch(`${API_BASE}/api/checkin`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    document.getElementById("checkin-response").textContent = data.message || "Check-in submitted!";
    document.getElementById("checkin-form").reset();
    fetchSummary();
    fetchTasks();
  } catch (err) {
    document.getElementById("checkin-response").textContent = "Error submitting check-in.";
  }
  setLoading("checkin-response", false);
});

// --- Add Task ---
document.getElementById("add-task-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const desc = document.getElementById("new-task-desc").value.trim();
  if (!desc) return;
  setLoading("add-task-form", true);
  try {
    const res = await fetch(`${API_BASE}/api/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ taskDescription: desc })
    });
    if (res.ok) {
      document.getElementById("add-task-form").reset();
      fetchTasks();
    } else {
      alert("Error adding task.");
    }
  } catch (err) {
    alert("Error adding task.");
  }
  setLoading("add-task-form", false);
});

// --- Fetch Tasks ---
async function fetchTasks() {
  setLoading("tasks-list", true);
  try {
    const res = await fetch(`${API_BASE}/api/tasks`);
    const data = await res.json();
    const list = document.getElementById("tasks-list");
    list.innerHTML = "";
    (data.tasks || []).forEach((task) => {
      const li = document.createElement("li");
      li.textContent = `${task.taskDescription} [${task.status}]`;
      if (task.status !== "Done") {
        const btn = document.createElement("button");
        btn.textContent = "Mark Done";
        btn.onclick = () => markTaskDone(task.id);
        li.appendChild(btn);
      }
      list.appendChild(li);
    });
  } catch (err) {
    document.getElementById("tasks-list").innerHTML = "<li>Error loading tasks.</li>";
  }
  setLoading("tasks-list", false);
}

// --- Mark Task as Done ---
async function markTaskDone(taskId) {
  setLoading("tasks-list", true);
  try {
    const res = await fetch(`${API_BASE}/api/tasks/${taskId}/done`, { method: "POST" });
    if (res.ok) fetchTasks();
    else alert("Error marking task as done.");
  } catch (err) {
    alert("Error marking task as done.");
  }
  setLoading("tasks-list", false);
}

// --- Fetch Summary ---
async function fetchSummary() {
  setLoading("summary-content", true);
  try {
    const res = await fetch(`${API_BASE}/api/summary`);
    const data = await res.json();
    document.getElementById("summary-content").textContent = data.summary?.message || "No summary.";
  } catch (err) {
    document.getElementById("summary-content").textContent = "Error loading summary.";
  }
  setLoading("summary-content", false);
}

// --- Utility: Loading State ---
function setLoading(id, loading) {
  const el = document.getElementById(id);
  if (!el) return;
  if (loading) el.classList.add("loading");
  else el.classList.remove("loading");
}

// --- Initial Load ---
fetchTasks();
fetchSummary();

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
