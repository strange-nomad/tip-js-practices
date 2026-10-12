"use strict";

const totalTasks = 12;
const completedTasks = 5;

// Проверка входных данных
if (
  typeof totalTasks !== "number" ||
  typeof completedTasks !== "number" ||
  !Number.isInteger(totalTasks) ||
  !Number.isInteger(completedTasks)
) {
  console.log("Ошибка: параметры должны быть целыми числами");
} else if (totalTasks < 0 || totalTasks > 1000) {
  console.log("Ошибка: общее количество задач должно быть от 0 до 1000");
} else if (completedTasks < 0 || completedTasks > totalTasks) {
  console.log("Ошибка: выполнено задач больше, чем существует, или число отрицательно");
} else if (totalTasks === 0 && completedTasks === 0) {
  console.log("Задач пока нет");
} else {
  const remainingTasks = totalTasks - completedTasks;
  const progressPercent = (completedTasks / totalTasks) * 100;

  let status = "В работе";
  if (completedTasks === 0) {
    status = "Не начато";
  } else if (completedTasks === totalTasks) {
    status = "Завершено";
  }

  console.log(`Всего задач: ${totalTasks}`);
  console.log(`Выполнено: ${completedTasks}`);
  console.log(`Осталось: ${remainingTasks}`);
  console.log(`Прогресс: ${progressPercent.toFixed(1)}%`);
  console.log(`Статус: ${status}`);
}
