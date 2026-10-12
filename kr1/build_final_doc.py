import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_doc_path = r"C:\Users\user\Desktop\ТИПЫ\КР1 ТИП (3 семестр).docx"
doc = Document(base_doc_path)

# 1. Заменяем шапку титульником
# Удаляем старые строки шапки (индексы 0-7: название и ФИО/Группа)
# Создаем титульный блок
p_title1 = doc.paragraphs[0]
p_title1.text = "Контрольная работа №1"
p_title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
run1 = p_title1.runs[0]
run1.font.bold = True
run1.font.size = Pt(16)
run1.font.name = "Times New Roman"

p_title2 = doc.paragraphs[1]
p_title2.text = "Основы JavaScript. Задания и отчёт"
p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p_title2.runs[0]
run2.font.bold = True
run2.font.size = Pt(14)
run2.font.name = "Times New Roman"

# Очистим параграфы 3-7 (где были старые подчеркивания)
for i in range(2, 8):
    doc.paragraphs[i].text = ""

# Вставим таблицу титульника после p_title2
table_data = [
    ("Дисциплина", "Технологии индустриального программирования"),
    ("Институт", "Перспективных технологий и индустриального программирования"),
    ("Кафедра", "Индустриального программирования"),
    ("Вид учебного материала", "Контрольная работа"),
    ("Преподаватель", "Евдошенко Олег Игоревич"),
    ("Студент", "Кабанов Арсений, группа ЭФБО-17-25"),
    ("Семестр", "3 семестр, 2026-2027"),
]

# Создаем таблицу
table = doc.add_table(rows=len(table_data), cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = 'Table Grid'

# Переместим таблицу наверх (сразу после p_title2)
p_title2._element.addnext(table._element)

for row_idx, (col1, col2) in enumerate(table_data):
    row = table.rows[row_idx]
    
    cell1 = row.cells[0]
    cell1.text = col1
    cell1.paragraphs[0].runs[0].font.name = "Times New Roman"
    cell1.paragraphs[0].runs[0].font.size = Pt(11)
    cell1.paragraphs[0].runs[0].font.bold = True
    cell1.width = Inches(2.3)
    
    cell2 = row.cells[1]
    cell2.text = col2
    cell2.paragraphs[0].runs[0].font.name = "Times New Roman"
    cell2.paragraphs[0].runs[0].font.size = Pt(11)
    if col1 in ["Дисциплина", "Институт", "Кафедра", "Студент"]:
        cell2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell2.width = Inches(4.2)

# Добавим разделитель после таблицы
p_space = doc.paragraphs[2]
p_space.text = ""

# 2. Подставляем листинги и скриншоты в соответствующие места
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

screenshots_dir = r"C:\Users\user\Desktop\ТИПЫ\kr1\screenshots"

for p in doc.paragraphs:
    if "[Вставьте progress.js.]" in p.text:
        p.text = "Листинг 1. Реализация progress.js:\n" + listing1_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте результаты трёх запусков с подписью.]" in p.text:
        p.text = "Скриншот 1. Результаты трёх проверочных запусков программы progress.js:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot1.png"), width=Inches(5.8))
    elif "[Вставьте demoTasks, функцию и два вызова.]" in p.text:
        p.text = "Листинг 2. Реализация отбора невыполненных задач:\n" + listing2_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте результаты отбора с подписью.]" in p.text:
        p.text = "Скриншот 2. Результаты отбора невыполненных задач из demoTasks и пустого массива []:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot2.png"), width=Inches(5.8))
    elif "[Вставьте функцию, необходимые вспомогательные функции и вызовы.]" in p.text:
        p.text = "Листинг 3. Функция setTaskCompleted и проверки:\n" + listing3_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте результаты двух проверок с подписью.]" in p.text:
        p.text = "Скриншот 3. Результаты проверки изменения статуса задачи и обработки ошибки (отказа):"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot3.png"), width=Inches(5.8))
    elif "[Вставьте относящийся к переключению код.]" in p.text:
        p.text = "Листинг 4. Обработчик события переключения статуса:\n" + listing4_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте состояние после переключения с подписью.]" in p.text:
        p.text = "Скриншот 4. Интерфейс приложения после переключения фильтра на «В работе» и отметки задачи id = 4:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot4.png"), width=Inches(5.8))
    elif "[Укажите, как определяется id и обновляется интерфейс.]" in p.text:
        p.text = explanation4_text
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(11)

final_path = r"C:\Users\user\Desktop\ТИПЫ\КР1_ЭФБО-17-25_КабановА.docx"
doc.save(final_path)
print("Успешно сформирован итоговый отчёт:", final_path)
