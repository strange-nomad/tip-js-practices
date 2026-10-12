import docx

doc = docx.Document(r"C:\Users\user\Desktop\ТИПЫ\КР1 ТИП (3 семестр).docx")

listing1_code = """\"use strict\";

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

// Проверочные вызовы:
showProgress(12, 5);
showProgress(0, 0);
showProgress(5, 6);"""

listing2_code = """\"use strict\";

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

// Проверочные вызовы:
const pendingFromDemo = getPendingTasks(demoTasks);
console.log("Идентификаторы невыполненных задач:", pendingFromDemo.map((t) => t.id));
console.log("Результат отбора из demoTasks:", pendingFromDemo);

const pendingFromEmpty = getPendingTasks([]);
console.log("Результат отбора из пустого массива []:", pendingFromEmpty);"""

listing3_code = """\"use strict\";

// Вспомогательная функция валидации идентификатора
function isValidId(id) {
  return typeof id === "number" && Number.isInteger(id) && id > 0 && id <= Number.MAX_SAFE_INTEGER;
}

// Функция изменения статуса задачи с сохранением иммутабельности
function setTaskCompleted(tasks, id, completed) {
  if (!Array.isArray(tasks)) {
    return { ok: false, error: "Параметр tasks должен быть массивом" };
  }

  if (!isValidId(id)) {
    return { ok: false, error: "Некорректный идентификатор задачи" };
  }

  if (typeof completed !== "boolean") {
    return { ok: false, error: "Статус задачи должен быть булевым значением" };
  }

  const taskIndex = tasks.findIndex((task) => task.id === id);
  if (taskIndex === -1) {
    return { ok: false, error: "Задача с указанным id не найдена" };
  }

  const updatedTasks = tasks.map((task) =>
    task.id === id ? { ...task, completed } : task
  );

  return { ok: true, tasks: updatedTasks };
}

// Проверочные вызовы:
// 1. Установка completed = true для id = 4
const resSuccess = setTaskCompleted(demoTasks, 4, true);
const updatedTask = resSuccess.tasks.find((t) => t.id === 4);
const originalTask = demoTasks.find((t) => t.id === 4);

console.log("Статус в возвращенном массиве (id: 4):", updatedTask.completed); // true
console.log("Статус в исходном массиве demoTasks (id: 4):", originalTask.completed); // false
console.log("Массив не мутирован:", resSuccess.tasks !== demoTasks);

// 2. Отдельный вызов с id = 777
const resError = setTaskCompleted(demoTasks, 777, true);
console.log("Результат отказа:", resError);"""

listing4_code = """// Фрагмент обработчика переключения статуса задачи в браузере
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

// Подключение делегированного обработчика к списку задач
elements.list.addEventListener("click", handleTaskListClick);"""

explanation4_text = "Пояснение. При клике на кнопку «Выполнена» делегированный обработчик события на контейнере списка через event.target.closest() находит целевую кнопку и считывает числовой идентификатор из dataset.taskId родительской карточки. По этому id вызывается функция setTaskCompleted, создающая обновлённый массив задач без мутации исходных данных, после чего функция renderApp() повторно отрисовывает видимый список в соответствии с текущим активным фильтром («В работе») и пересчитывает общую сводку."

for p in doc.paragraphs:
    if "[Вставьте progress.js.]" in p.text:
        p.text = "Листинг 1. Реализация progress.js:\n" + listing1_code
    elif "[Вставьте demoTasks, функцию и два вызова.]" in p.text:
        p.text = "Листинг 2. Реализация отбора невыполненных задач:\n" + listing2_code
    elif "[Вставьте функцию, необходимые вспомогательные функции и вызовы.]" in p.text:
        p.text = "Листинг 3. Функция setTaskCompleted и вспомогательная валидация:\n" + listing3_code
    elif "[Вставьте относящийся к переключению код.]" in p.text:
        p.text = "Листинг 4. Обработчик переключения статуса:\n" + listing4_code
    elif "[Укажите, как определяется id и обновляется интерфейс.]" in p.text:
        p.text = explanation4_text

out_path = r"C:\Users\user\Desktop\ТИПЫ\КР1_Заполненная_Шаблон.docx"
doc.save(out_path)
print("Saved to", out_path)
