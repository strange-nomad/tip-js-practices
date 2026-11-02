"use strict";

// Функция валидации черновика задачи (фрагмент validateTaskDraft из ПР4)
function validateTaskDraft(draft, tasks, editingId = null) {
  const errors = {};

  // 1. Проверка и нормализация названия (1..100 символов после trim)
  let validTitle = null;
  if (typeof draft.title !== "string") {
    errors.title = "Название должно быть строкой";
  } else {
    const trimmed = draft.title.trim();
    if (trimmed.length < 1 || trimmed.length > 100) {
      errors.title = "Длина названия должна быть от 1 до 100 символов";
    } else {
      validTitle = trimmed;
    }
  }

  const ok = Object.keys(errors).length === 0;
  return ok
    ? {
        ok: true,
        value: {
          id: Number(draft.id),
          title: validTitle,
          priority: draft.priority,
        },
      }
    : {
        ok: false,
        errors,
      };
}

// Проверочные вызовы для Контрольной работы № 2:
const tasks = [];

console.log("=== Вызов 1: title = '  Изучить localStorage  ' ===");
const res1 = validateTaskDraft(
  { id: "20", title: "  Изучить localStorage  ", priority: "high" },
  tasks
);
console.log(JSON.stringify(res1, null, 2));

console.log("\n=== Вызов 2: title = '   ' ===");
const res2 = validateTaskDraft(
  { id: "20", title: "   ", priority: "high" },
  tasks
);
console.log(JSON.stringify(res2, null, 2));
