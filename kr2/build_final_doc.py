import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

base_doc_path = r"C:\Users\user\Desktop\ТИПЫ\КР2 ТИП (3 семестр).docx"
doc = Document(base_doc_path)

# 1. Заменяем шапку титульным блоком
p_title1 = doc.paragraphs[0]
p_title1.text = "Контрольная работа №2"
p_title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
run1 = p_title1.runs[0]
run1.font.bold = True
run1.font.size = Pt(16)
run1.font.name = "Times New Roman"

p_title2 = doc.paragraphs[1]
p_title2.text = "Формы, хранение данных и API. Задания и отчёт"
p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p_title2.runs[0]
run2.font.bold = True
run2.font.size = Pt(14)
run2.font.name = "Times New Roman"

# Очистим параграфы с подстрочниками (ФИО, группа, дата)
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

table = doc.add_table(rows=len(table_data), cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = 'Table Grid'
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

# Листинги кода:
listing1_code = """// Фрагмент validateTaskDraft: проверка и нормализация названия
export function validateTaskDraft(draft, tasks, editingId = null) {
  const errors = {};

  // Проверка и нормализация названия задачи (1..100 символов после trim)
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
    ? { ok: true, value: { id: Number(draft.id), title: validTitle, priority: draft.priority } }
    : { ok: false, errors };
}

// Проверочные вызовы:
const tasks = [];

// Вызов 1: валидное название с краевыми пробелами
const resultValid = validateTaskDraft(
  { id: "20", title: "  Изучить localStorage  ", priority: "high" },
  tasks
);
console.log("Вызов 1 (валидное название):", resultValid);

// Вызов 2: невалидное название (только пробелы)
const resultInvalid = validateTaskDraft(
  { id: "20", title: "   ", priority: "high" },
  tasks
);
console.log("Вызов 2 (пустая строка):", resultInvalid);"""

listing2_code = """// Фрагменты модуля task-storage.js: чтение и запись JSON в localStorage
export const STORAGE_VERSION = 1;

export function loadTasks(storage, key, fallbackTasks) {
  let raw;
  try {
    raw = storage.getItem(key);
  } catch (error) {
    return { ok: false, source: "fallback", tasks: fallbackTasks.map(t => ({ ...t })) };
  }
  if (raw === null || raw === undefined) {
    return { ok: true, source: "initial", tasks: fallbackTasks.map(t => ({ ...t })) };
  }
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || parsed.version !== STORAGE_VERSION || !isValidTaskList(parsed.tasks)) {
      return { ok: false, source: "fallback", tasks: fallbackTasks.map(t => ({ ...t })) };
    }
    return { ok: true, source: "storage", tasks: parsed.tasks.map(t => ({ ...t })) };
  } catch (error) {
    return { ok: false, source: "fallback", tasks: fallbackTasks.map(t => ({ ...t })) };
  }
}

export function saveTasks(storage, key, tasks) {
  if (!isValidTaskList(tasks)) return { ok: false, error: "Недопустимый список задач" };
  try {
    storage.setItem(key, JSON.stringify({ version: STORAGE_VERSION, tasks }));
    return { ok: true };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}

// Места вызова в main.js:
// 1. Восстановление данных при инициализации страницы:
const loaded = loadTasks(window.localStorage, storageKey, initialTasks);
let currentTasks = loaded.tasks;

// 2. Сохранение обновленного списка при добавлении задачи (включая id = 20):
currentTasks.push(newTask);
saveTasks(window.localStorage, storageKey, currentTasks);
renderApp();"""

listing3_code = """// Настройка API-клиента и метод getTasks с передачей query-параметров на сервер
export function createTaskApi(client) {
  async function getTasks(filters = {}) {
    const query = {};
    if ("completed" in filters) query.completed = filters.completed;
    if ("priority" in filters) query.priority = filters.priority;
    if ("categoryId" in filters) query.categoryId = filters.categoryId;
    if ("q" in filters) query.q = filters.q;

    // Запрос отправляется на сервер с параметрами в строке запроса: /tasks?completed=false&priority=high
    const result = await client.requestJson("/tasks", { query });
    return { tasks: result.data, meta: result.meta };
  }
  return { getTasks };
}

// Настройка клиента и проверочный вызов:
const client = createApiClient({ baseUrl: "http://localhost:3000/api" });
const api = createTaskApi(client);

const { tasks, meta } = await api.getTasks({ completed: false, priority: "high" });

console.log("Полученные идентификаторы задач (id):", tasks.map(t => t.id)); // [4, 13, 34]
console.log("Метаданные (meta.total):", meta.total); // 3"""

listing4_code = """// 1. Ветка проверки response.ok в api-client.js (метод requestJson):
if (response.ok) {
  return await response.json();
}

// При HTTP-ошибке (статусы 4xx / 5xx) формируется структурированная ошибка ApiError:
let errorPayload = null;
try {
  errorPayload = JSON.parse(await response.text());
} catch {}

const message = errorPayload?.error?.message || `HTTP ошибка ${response.status}`;
throw new ApiError(message, {
  kind: "http",
  status: response.status,
  code: errorPayload?.error?.code ?? null,
  url,
});

// 2. Вызов getTaskById(999) с перехватом ошибки через try/catch:
try {
  await api.getTaskById(999);
} catch (error) {
  if (error instanceof ApiError) {
    console.log("Успешный перехват ошибки:");
    console.log("kind:", error.kind);     // "http"
    console.log("status:", error.status); // 404
  } else {
    console.error("Непредвиденная ошибка:", error);
  }
}"""

explanation4_text = "Клиент явно проверяет HTTP-статус через response.ok, поскольку функция fetch() отклоняет промис только при сбое сети или тайм-ауте, а при ошибочных ответах сервера (таких как 404 или 500) успешно возвращает объект Response, который клиенту необходимо распознать и корректно обработать без аварийного падения приложения."

listing5_code = """// 1. Контроллер: функция toggleTask и обертка мутации с последующей перезагрузкой
async function toggleTask(id) {
  const target = tasks.find((t) => t.id === id);
  if (!target) return;

  await performMutation(async () => {
    // Вызов API для обновления completed через PATCH
    await api.setTaskCompleted(id, !target.completed);
    view.notify("Статус задачи обновлен.", "success");
  });
}

async function performMutation(action) {
  view.setMutationPending(true);
  try {
    await action();
    // Повторный запрос актуальных данных с текущим фильтром (GET /api/tasks?completed=false)
    await loadData(false);
  } catch (error) {
    view.notify(messageForError(error), "error");
  } finally {
    view.setMutationPending(false);
  }
}

// 2. Метод API-клиента: отправка PATCH /api/tasks/:id
async function setTaskCompleted(id, completed, options = {}) {
  const response = await client.requestJson(`/tasks/${id}`, {
    method: "PATCH",
    body: { completed },
    signal: options?.signal,
  });
  return response.data;
}"""

screenshots_dir = r"C:\Users\user\Desktop\ТИПЫ\kr2\screenshots"

for p in doc.paragraphs:
    if "[Вставьте проверку названия и два вызова.]" in p.text:
        p.text = "Листинг 1. Проверка и нормализация названия задачи в validateTaskDraft:\n" + listing1_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте результаты обоих вызовов с подписью.]" in p.text:
        p.text = "Скриншот 1. Результаты двух проверочных вызовов validateTaskDraft:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot1.png"), width=Inches(5.8))
    elif "[Вставьте фрагменты сохранения, восстановления и их вызовы.]" in p.text:
        p.text = "Листинг 2. Чтение, запись JSON в localStorage и места вызовов:\n" + listing2_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Покажите задачу и запись хранилища после перезагрузки.]" in p.text:
        p.text = "Скриншот 2. Сохранённая задача в списке и открытая запись localStorage после перезагрузки:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot2.png"), width=Inches(5.8))
    elif "[Вставьте getTasks, настройку клиента и проверочный вызов.]" in p.text:
        p.text = "Листинг 3. Метод getTasks с query-параметрами и проверочный вызов:\n" + listing3_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Вставьте результат запроса с подписью.]" in p.text:
        p.text = "Скриншот 3. Результат запроса getTasks({ completed: false, priority: \"high\" }):"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot3.png"), width=Inches(5.8))
    elif "[Вставьте проверку HTTP-статуса и вызов с перехватом ошибки.]" in p.text:
        p.text = "Листинг 4. Проверка response.ok в клиенте и вызов getTaskById(999) с перехватом ошибки:\n" + listing4_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Покажите kind и status.]" in p.text:
        p.text = "Скриншот 4. Результат перехвата HTTP 404 (значения kind и status):"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot4.png"), width=Inches(5.8))
        
        # Параграф пояснения
        p_exp = doc.add_paragraph()
        img_p._element.addnext(p_exp._element)
        p_exp.text = "Пояснение: " + explanation4_text
        p_exp.runs[0].font.name = "Times New Roman"
        p_exp.runs[0].font.size = Pt(11)
    elif "[Вставьте код изменения через API и последующей загрузки.]" in p.text:
        p.text = "Листинг 5. Код изменения через API (PATCH) и последующей перезагрузки (GET):\n" + listing5_code
        p.runs[0].font.name = "Consolas"
        p.runs[0].font.size = Pt(9.5)
    elif "[Покажите результат и запросы PATCH → GET.]" in p.text:
        p.text = "Скриншот 5. Панель Network (цепочка PATCH → GET) и список после исключения задачи 4:"
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot5.png"), width=Inches(5.8))

final_path = r"C:\Users\user\Desktop\ТИПЫ\КР2_ЭФБО-17-25_КабановА.docx"
doc.save(final_path)
print("Итоговый документ КР2 успешно сохранён:", final_path)
