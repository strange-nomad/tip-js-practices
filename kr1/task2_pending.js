"use strict";

// Исходный контрольный набор задач из ПР2–ПР3
const demoTasks = [
  { id: 1, title: "Изучить функции", completed: true, priority: "medium" },
  { id: 4, title: "Подготовить модель задач", completed: false, priority: "high" },
  { id: 7, title: "Проверить методы массивов", completed: false, priority: "low" },
  { id: 10, title: "Оформить README", completed: true, priority: "medium" },
];

// Функция отбора невыполненных задач
function getPendingTasks(tasks) {
  return tasks.filter((task) => task.completed === false);
}

// Проверочные вызовы для Контрольной работы № 1:
console.log("--- 1. Отбор из demoTasks ---");
const pendingDemo = getPendingTasks(demoTasks);
console.log("Результат (id):", pendingDemo.map((t) => t.id));
console.log("Объекты невыполненных задач:", pendingDemo);

console.log("\n--- 2. Отбор из пустого массива [] ---");
const pendingEmpty = getPendingTasks([]);
console.log("Результат для []:", pendingEmpty);
