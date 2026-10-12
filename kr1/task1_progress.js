"use strict";

// Функция вывода сводки выполнения задач
function showProgress(totalTasks, completedTasks) {
  // 1. Проверка типов данных и целочисленности
  if (
    typeof totalTasks !== "number" ||
    typeof completedTasks !== "number" ||
    !Number.isInteger(totalTasks) ||
    !Number.isInteger(completedTasks)
  ) {
    console.log("Ошибка: параметры должны быть целыми числами");
    return;
  }

  // 2. Проверка диапазона
  if (totalTasks < 0 || totalTasks > 1000) {
    console.log("Ошибка: общее количество задач должно быть от 0 до 1000");
    return;
  }

  if (completedTasks < 0 || completedTasks > totalTasks) {
    console.log("Ошибка: выполнено задач больше, чем существует, или число отрицательно");
    return;
  }

  // 3. Обработка случая отсутствия задач
  if (totalTasks === 0 && completedTasks === 0) {
    console.log("Задач пока нет");
    return;
  }

  // 4. Расчет показателей
  const remainingTasks = totalTasks - completedTasks;
  const progressPercent = (completedTasks / totalTasks) * 100;

  // 5. Определение статуса по исходным количествам
  let status = "В работе";
  if (completedTasks === 0) {
    status = "Не начато";
  } else if (completedTasks === totalTasks) {
    status = "Завершено";
  }

  // 6. Вывод результата
  console.log(`Всего задач: ${totalTasks}`);
  console.log(`Выполнено: ${completedTasks}`);
  console.log(`Осталось: ${remainingTasks}`);
  console.log(`Прогресс: ${progressPercent.toFixed(1)}%`);
  console.log(`Статус: ${status}`);
}

// Проверочные запуски для Контрольной работы № 1:
console.log("--- Проверка 1: (12, 5) ---");
showProgress(12, 5);

console.log("\n--- Проверка 2: (0, 0) ---");
showProgress(0, 0);

console.log("\n--- Проверка 3: (5, 6) ---");
showProgress(5, 6);
