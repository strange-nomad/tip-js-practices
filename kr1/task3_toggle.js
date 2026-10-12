"use strict";

const demoTasks = [
  { id: 1, title: "Изучить функции", completed: true, priority: "medium" },
  { id: 4, title: "Подготовить модель задач", completed: false, priority: "high" },
  { id: 7, title: "Проверить методы массивов", completed: false, priority: "low" },
  { id: 10, title: "Оформить README", completed: true, priority: "medium" },
];

// Вспомогательная функция валидации идентификатора
function isValidId(id) {
  return typeof id === "number" && Number.isInteger(id) && id > 0 && id <= Number.MAX_SAFE_INTEGER;
}

// Функция изменения статуса задачи
function setTaskCompleted(tasks, id, completed) {
  if (!Array.isArray(tasks)) {
    return { ok: false, error: "Параметр tasks должен быть массивом" };
  }

  if (!isValidId(id)) {
    return { ok: false, error: "Некорректный идентификатор задачи" };
  }

  if (typeof completed !== "boolean") {
    return { ok: false, error: "Статус задачи должен быть булевым значением (true/false)" };
  }

  const taskIndex = tasks.findIndex((task) => task.id === id);
  if (taskIndex === -1) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  // Создаем новый массив и новый объект измененной задачи (иммутабельность)
  const updatedTasks = tasks.map((task) =>
    task.id === id ? { ...task, completed } : task
  );

  return { ok: true, tasks: updatedTasks };
}

// Проверочные вызовы для Контрольной работы № 1:

console.log("--- Проверка 1: Установка completed = true для id = 4 ---");
const resultSuccess = setTaskCompleted(demoTasks, 4, true);

if (resultSuccess.ok) {
  const updatedTask = resultSuccess.tasks.find((t) => t.id === 4);
  const originalTask = demoTasks.find((t) => t.id === 4);

  console.log("Статус в новом массиве (id: 4):", updatedTask.completed); // true
  console.log("Статус в исходном массиве (id: 4):", originalTask.completed); // false
  console.log("Массив не мутирован (ссылки не равны):", resultSuccess.tasks !== demoTasks);
}

console.log("\n--- Проверка 2: Попытка изменения отсутствующей задачи id = 777 ---");
const resultError = setTaskCompleted(demoTasks, 777, true);
console.log("Результат отказа:", resultError);
