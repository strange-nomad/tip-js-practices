// Валидация положительного безопасного целочисленного id
function validateId(id) {
  if (typeof id !== "number" || !Number.isInteger(id) || id <= 0 || id > Number.MAX_SAFE_INTEGER) {
    return { ok: false, error: "Некорректный идентификатор: ожидается положительное безопасное целое число" };
  }
  return { ok: true };
}

// Валидация названия (строка 1..100 символов после trim)
function validateTitle(title) {
  if (typeof title !== "string") {
    return { ok: false, error: "Название должно быть строкой" };
  }
  const trimmed = title.trim();
  if (trimmed.length < 1 || trimmed.length > 100) {
    return { ok: false, error: "Длина названия должна быть от 1 до 100 символов" };
  }
  return { ok: true, title: trimmed };
}

// Валидация приоритета
function validatePriority(priority) {
  const allowed = ["low", "medium", "high"];
  if (!allowed.includes(priority)) {
    return { ok: false, error: "Недопустимый приоритет: ожидается low, medium или high" };
  }
  return { ok: true };
}

// Создание новой задачи
export function createTask(id, title, priority = "medium") {
  const idCheck = validateId(id);
  if (!idCheck.ok) return idCheck;

  const titleCheck = validateTitle(title);
  if (!titleCheck.ok) return titleCheck;

  const priorityCheck = validatePriority(priority);
  if (!priorityCheck.ok) return priorityCheck;

  return {
    ok: true,
    task: {
      id,
      title: titleCheck.title,
      completed: false,
      priority,
    },
  };
}

// Поиск задачи по id
export function findTaskById(tasks, id) {
  return tasks.find((task) => task.id === id);
}

// Фильтрация невыполненных задач
export function getPendingTasks(tasks) {
  return tasks.filter((task) => task.completed === false);
}

// Получение массива названий
export function getTaskTitles(tasks) {
  return tasks.map((task) => task.title);
}

// Расчет статистики
export function getTaskStats(tasks) {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed === true).length;
  const pending = total - completed;
  const progress = total === 0 ? 0 : (completed / total) * 100;
  return { total, completed, pending, progress };
}

// Добавление задачи без мутации исходного массива
export function addTask(tasks, id, title, priority = "medium") {
  const created = createTask(id, title, priority);
  if (!created.ok) return created;

  if (tasks.some((task) => task.id === id)) {
    return { ok: false, error: "Задача с таким id уже существует" };
  }

  return {
    ok: true,
    tasks: [...tasks, created.task],
  };
}

// Изменение статуса задачи (иммутабельно)
export function setTaskCompleted(tasks, id, completed) {
  const idCheck = validateId(id);
  if (!idCheck.ok) return idCheck;

  if (typeof completed !== "boolean") {
    return { ok: false, error: "Статус должен быть булевым значением (true/false)" };
  }

  const existing = findTaskById(tasks, id);
  if (!existing) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  return {
    ok: true,
    tasks: tasks.map((task) => (task.id === id ? { ...task, completed } : task)),
  };
}

// Переименование задачи
export function renameTask(tasks, id, title) {
  const idCheck = validateId(id);
  if (!idCheck.ok) return idCheck;

  const titleCheck = validateTitle(title);
  if (!titleCheck.ok) return titleCheck;

  const existing = findTaskById(tasks, id);
  if (!existing) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  return {
    ok: true,
    tasks: tasks.map((task) => (task.id === id ? { ...task, title: titleCheck.title } : task)),
  };
}

// Удаление задачи
export function removeTask(tasks, id) {
  const idCheck = validateId(id);
  if (!idCheck.ok) return idCheck;

  const existing = findTaskById(tasks, id);
  if (!existing) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  return {
    ok: true,
    tasks: tasks.filter((task) => task.id !== id),
  };
}

// Обновление названия и приоритета задачи без мутации
export function updateTask(tasks, id, title, priority) {
  const idCheck = validateId(id);
  if (!idCheck.ok) return idCheck;

  const existing = findTaskById(tasks, id);
  if (!existing) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  const titleCheck = validateTitle(title);
  if (!titleCheck.ok) return titleCheck;

  const priorityCheck = validatePriority(priority);
  if (!priorityCheck.ok) return priorityCheck;

  return {
    ok: true,
    tasks: tasks.map((task) =>
      task.id === id
        ? { ...task, title: titleCheck.title, priority }
        : task
    ),
  };
}
