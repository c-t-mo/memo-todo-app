const form = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const taskList = document.getElementById("task-list");
const errorMessage = document.getElementById("error-message");

async function fetchTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  tasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task-item" + (task.done ? " done" : "");

    li.innerHTML = `
      <div class="task-main" data-id="${task.id}">
        <p class="task-title">${escapeHtml(task.title)}</p>
        ${task.content ? `<p class="task-content">${escapeHtml(task.content)}</p>` : ""}
        <p class="task-time">${task.created_at}</p>
      </div>
      <button class="delete-btn" data-id="${task.id}">🗑</button>
    `;
    taskList.appendChild(li);
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMessage.textContent = "";

  const title = titleInput.value.trim();
  const content = contentInput.value.trim();

  const res = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });

  if (!res.ok) {
    const data = await res.json();
    errorMessage.textContent = data.error || "追加に失敗しました";
    return;
  }

  titleInput.value = "";
  contentInput.value = "";
  fetchTasks();
});

taskList.addEventListener("click", async (e) => {
  const deleteId = e.target.closest(".delete-btn")?.dataset.id;
  const toggleId = e.target.closest(".task-main")?.dataset.id;

  if (deleteId) {
    await fetch(`/api/tasks/${deleteId}`, { method: "DELETE" });
    fetchTasks();
    return;
  }

  if (toggleId) {
    await fetch(`/api/tasks/${toggleId}/toggle`, { method: "PATCH" });
    fetchTasks();
  }
});

fetchTasks();
