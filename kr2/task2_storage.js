"use strict";

export const STORAGE_VERSION = 1;

// Валидация списка задач
function isValidTaskList(value) {
  if (!Array.isArray(value)) return false;
  return value.every(
    (t) =>
      t &&
      typeof t === "object" &&
      typeof t.id === "number" &&
      typeof t.title === "string" &&
      typeof t.completed === "boolean" &&
      ["low", "medium", "high"].includes(t.priority)
  );
}

// Загрузка задач из localStorage
export function loadTasks(storage, key, fallbackTasks) {
  const fallbackCopy = fallbackTasks.map((task) => ({ ...task }));
  let raw;
  try {
    raw = storage.getItem(key);
  } catch (error) {
    return { ok: false, source: "fallback", tasks: fallbackCopy, error: error.message };
  }

  if (raw === null || raw === undefined) {
    return { ok: true, source: "initial", tasks: fallbackCopy };
  }

  try {
    const parsed = JSON.parse(raw);
    if (
      !parsed ||
      typeof parsed !== "object" ||
      parsed.version !== STORAGE_VERSION ||
      !isValidTaskList(parsed.tasks)
    ) {
      return { ok: false, source: "fallback", tasks: fallbackCopy, error: "Некорректная структура JSON" };
    }
    return { ok: true, source: "storage", tasks: parsed.tasks.map((task) => ({ ...task })) };
  } catch (error) {
    return { ok: false, source: "fallback", tasks: fallbackCopy, error: error.message };
  }
}

// Сохранение задач в localStorage в формате { version: 1, tasks: [...] }
export function saveTasks(storage, key, tasks) {
  if (!isValidTaskList(tasks)) {
    return { ok: false, error: "Некорректный список задач" };
  }
  try {
    storage.setItem(key, JSON.stringify({ version: STORAGE_VERSION, tasks }));
    return { ok: true };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}
