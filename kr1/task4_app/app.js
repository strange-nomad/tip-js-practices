"use strict";

// Исходный контрольный набор demoTasks из ПР2–ПР3
const demoTasks = [
  { id: 1, title: "Изучить функции", completed: true, priority: "medium" },
  { id: 4, title: "Подготовить модель задач", completed: false, priority: "high" },
  { id: 7, title: "Проверить методы массивов", completed: false, priority: "low" },
  { id: 10, title: "Оформить README", completed: true, priority: "medium" },
];

let currentTasks = demoTasks.map((task) => ({ ...task }));
let currentFilter = "all";

const priorityLabels = {
  low: "Низкий",
  medium: "Средний",
  high: "Высокий",
};

const elements = {
  list: document.querySelector("#task-list"),
  filters: document.querySelector("#task-filters"),
  summary: document.querySelector("#task-summary"),
  empty: document.querySelector("#empty-message"),
  message: document.querySelector("#operation-message"),
};

// Функция изменения статуса задачи (из ПР2 / Задание 3)
function setTaskCompleted(tasks, id, completed) {
  if (!Array.isArray(tasks)) return { ok: false, error: "tasks не массив" };
  const taskIndex = tasks.findIndex((t) => t.id === id);
  if (taskIndex === -1) return { ok: false, error: "Задача не найдена" };

  const updatedTasks = tasks.map((task) =>
    task.id === id ? { ...task, completed } : task
  );
  return { ok: true, tasks: updatedTasks };
}

// Фильтрация видимых задач
function getVisibleTasks(tasks, filter) {
  if (filter === "pending") return tasks.filter((t) => !t.completed);
  if (filter === "completed") return tasks.filter((t) => t.completed);
  return [...tasks];
}

// Создание DOM-элемента карточки
function createTaskElement(task) {
  const li = document.createElement("li");
  li.className = `task-card${task.completed ? " is-completed" : ""}`;
  li.dataset.taskId = String(task.id);

  const title = document.createElement("h3");
  title.className = "task-title";
  title.textContent = task.title;

  const status = document.createElement("span");
  status.className = "task-status";
  status.textContent = task.completed ? "Выполнена" : "В работе";

  const priority = document.createElement("span");
  priority.className = "task-priority";
  priority.textContent = `Приоритет: ${priorityLabels[task.priority] ?? task.priority}`;

  const actions = document.createElement("div");
  actions.className = "task-actions";

  const toggleBtn = document.createElement("button");
  toggleBtn.type = "button";
  toggleBtn.dataset.action = "toggle";
  toggleBtn.setAttribute("aria-pressed", String(task.completed));
  toggleBtn.innerHTML = `<span class="action-label">${task.completed ? "Вернуть в работу" : "Выполнена"}</span>`;

  const deleteBtn = document.createElement("button");
  deleteBtn.type = "button";
  deleteBtn.dataset.action = "delete";
  deleteBtn.innerHTML = `<span class="action-label">Удалить</span>`;

  actions.append(toggleBtn, deleteBtn);
  li.append(title, status, priority, actions);
  return li;
}

// Обновление сводки
function renderSummary(tasks, visibleCount) {
  const total = tasks.length;
  const completed = tasks.filter((t) => t.completed).length;
  const pending = total - completed;
  const progress = total > 0 ? (completed / total) * 100 : 0;

  elements.summary.querySelector('[data-stat="total"]').textContent = String(total);
  elements.summary.querySelector('[data-stat="completed"]').textContent = String(completed);
  elements.summary.querySelector('[data-stat="pending"]').textContent = String(pending);
  elements.summary.querySelector('[data-stat="progress"]').textContent = `${progress.toFixed(1)}%`;
  elements.summary.querySelector('[data-stat="visible"]').textContent = String(visibleCount);
}

// Перерисовка всего интерфейса
function renderApp() {
  const visible = getVisibleTasks(currentTasks, currentFilter);
  elements.list.replaceChildren(...visible.map(createTaskElement));
  renderSummary(currentTasks, visible.length);

  // Обновление состояния кнопок фильтров
  for (const button of elements.filters.querySelectorAll("button")) {
    const isActive = button.dataset.filter === currentFilter;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  }
}

// =============================================================================
// ОБРАБОТЧИК ПЕРЕКЛЮЧЕНИЯ СТАТУСА (ДЛЯ ЛИСТИНГА 4 В ОТЧЁТЕ КР1):
// =============================================================================
function handleTaskListClick(event) {
  const toggleBtn = event.target.closest('button[data-action="toggle"]');
  if (!toggleBtn || !elements.list.contains(toggleBtn)) return;

  const card = toggleBtn.closest("[data-task-id]");
  const taskId = Number(card?.dataset?.taskId);

  const task = currentTasks.find((t) => t.id === taskId);
  if (!task) return;

  const result = setTaskCompleted(currentTasks, taskId, !task.completed);
  if (result.ok) {
    currentTasks = result.tasks;
    renderApp();
  }
}

// Переключение фильтра
function handleFilterClick(event) {
  const filterBtn = event.target.closest("button[data-filter]");
  if (!filterBtn) return;
  currentFilter = filterBtn.dataset.filter;
  renderApp();
}

// Подключение обработчиков событий
elements.list.addEventListener("click", handleTaskListClick);
elements.filters.addEventListener("click", handleFilterClick);

// Начальная отрисовка
renderApp();
