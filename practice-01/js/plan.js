"use strict";

const totalTasks = 12;
const completedTasks = 5;
const dailyLimit = 3;

// Проверка входных данных
if (
  typeof totalTasks !== "number" ||
  typeof completedTasks !== "number" ||
  !Number.isInteger(totalTasks) ||
  !Number.isInteger(completedTasks)
) {
  console.log("Ошибка: общее и выполненное количество задач должны быть целыми числами");
} else if (totalTasks < 0 || totalTasks > 1000) {
  console.log("Ошибка: общее количество задач должно быть от 0 до 1000");
} else if (completedTasks < 0 || completedTasks > totalTasks) {
  console.log("Ошибка: некорректное число выполненных задач");
} else if (
  typeof dailyLimit !== "number" ||
  !Number.isInteger(dailyLimit) ||
  dailyLimit < 1 ||
  dailyLimit > 1000
) {
  console.log("Ошибка: дневная норма должна быть целым числом от 1 до 1000");
} else {
  let remaining = totalTasks - completedTasks;
  console.log(`Осталось задач: ${remaining}`);

  if (remaining === 0) {
    console.log("Все задачи уже выполнены");
    console.log("Потребуется дней: 0");
  } else {
    let day = 0;
    while (remaining > 0) {
      day += 1;
      const tasksToday = Math.min(remaining, dailyLimit);
      remaining -= tasksToday;
      console.log(`День ${day}: выполнено ${tasksToday}, осталось ${remaining}`);
    }
    console.log(`Потребуется дней: ${day}`);
  }
}
