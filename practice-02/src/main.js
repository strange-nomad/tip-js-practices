import { demoTasks, variantNumber, variantTasks } from "./data.js";
import {
  findTaskById,
  getPendingTasks,
  getTaskTitles,
  getTaskStats,
  addTask,
  setTaskCompleted,
  renameTask,
  removeTask,
} from "./task-service.js";

function printStats(label, stats) {
  console.log(`${label}: всего ${stats.total}, выполнено ${stats.completed}, осталось ${stats.pending}, прогресс ${stats.progress.toFixed(1)}%`);
}

console.log("ПР2. Модуль задач (Вариант 1: Подготовка учебного проекта)\n");

// 1. Общий набор (demoTasks)
console.log("=== 1. Проверка общего набора ===");
let currentDemo = demoTasks;
printStats("1.1. Исходное состояние", getTaskStats(currentDemo));

const addRes = addTask(currentDemo, 20, "Новая задача", "high");
if (addRes.ok) {
  currentDemo = addRes.tasks;
  printStats("1.2. Добавлена задача id=20", getTaskStats(currentDemo));
}

const completeRes = setTaskCompleted(currentDemo, 4, true);
if (completeRes.ok) {
  currentDemo = completeRes.tasks;
  printStats("1.3. Задача id=4 завершена", getTaskStats(currentDemo));
}

const renameRes = renameTask(currentDemo, 10, "Оформить и проверить README");
if (renameRes.ok) {
  currentDemo = renameRes.tasks;
  printStats("1.4. Задача id=10 переименована", getTaskStats(currentDemo));
}

const removeRes = removeTask(currentDemo, 7);
if (removeRes.ok) {
  currentDemo = removeRes.tasks;
  printStats("1.5. Задача id=7 удалена", getTaskStats(currentDemo));
}

console.log("Названия задач после цепочки:", getTaskTitles(currentDemo));
console.log("Иммутабельность demoTasks (длина 4):", demoTasks.length === 4);

// 2. Индивидуальный вариант 1
console.log("\n=== 2. Проверка Варианта 1 ===");
let currentVariant = variantTasks;
printStats("2.1. Исходное состояние варианта 1", getTaskStats(currentVariant));

// Шаг 2: Добавление id = 80 с приоритетом high (для вар. 1)
const varAdd = addTask(currentVariant, 80, "Подготовить итоговый отчет", "high");
if (varAdd.ok) {
  currentVariant = varAdd.tasks;
  printStats("2.2. Добавлена задача id=80 (high)", getTaskStats(currentVariant));
}

// Шаг 3: Завершение задачи id = 11
const varComp = setTaskCompleted(currentVariant, 11, true);
if (varComp.ok) {
  currentVariant = varComp.tasks;
  printStats("2.3. Задача id=11 завершена", getTaskStats(currentVariant));
}

// Шаг 4: Переименование id = 23
const varRename = renameTask(currentVariant, 23, "Уточнить структуру модулей приложения");
if (varRename.ok) {
  currentVariant = varRename.tasks;
  printStats("2.4. Задача id=23 переименована", getTaskStats(currentVariant));
}

// Шаг 5: Удаление id = 37
const varRemove = removeTask(currentVariant, 37);
if (varRemove.ok) {
  currentVariant = varRemove.tasks;
  printStats("2.5. Задача id=37 удалена", getTaskStats(currentVariant));
}

// Шаг 6: Повторное добавление id = 80
const duplicateRes = addTask(currentVariant, 80, "Дубликат 80", "low");
console.log("2.6. Повторный id=80 корректно отклонен:", duplicateRes.ok === false ? `Отказ: "${duplicateRes.error}"` : "Ошибка!");

// Шаг 7: Проверка иммутабельности variantTasks
console.log("2.7. Иммутабельность variantTasks (длина 6):", variantTasks.length === 6);
printStats("Итог варианта 1", getTaskStats(currentVariant));
console.log("Названия задач:", getTaskTitles(currentVariant));
