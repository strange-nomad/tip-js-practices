import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_doc_path = r"C:\Users\user\Desktop\ТИПЫ\КР3 ТИП (3 семестр).docx"
output_path = r"C:\Users\user\Desktop\ТИПЫ\КР3_ЭФБО-17-25_КабановА.docx"
screenshots_dir = r"C:\Users\user\Desktop\ТИПЫ\kr3\screenshots"

doc = Document(base_doc_path)

# 1. Убираем колонтитулы (надписи сверху)
for section in doc.sections:
    for p in section.header.paragraphs:
        p.text = ""

# 2. Титульный блок
p_title1 = doc.paragraphs[0]
p_title1.text = "Контрольная работа № 3"
p_title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
run1 = p_title1.runs[0]
run1.font.bold = True
run1.font.size = Pt(16)
run1.font.name = "Times New Roman"

p_title2 = doc.paragraphs[1]
p_title2.text = "React-компоненты, интеграция с API и серверная разработка на Node.js. Задания и отчёт"
p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p_title2.runs[0]
run2.font.bold = True
run2.font.size = Pt(13)
run2.font.name = "Times New Roman"

# Очищаем строки подчеркиваний (ФИО, группа, дата)
for i in range(2, 8):
    if i < len(doc.paragraphs):
        doc.paragraphs[i].text = ""

# Таблица титульника со сведениями о студенте
table_data = [
    ("Дисциплина", "Технологии индустриального программирования"),
    ("Институт", "Перспективных технологий и индустриального программирования"),
    ("Кафедра", "Индустриального программирования"),
    ("Вид учебного материала", "Контрольная работа № 3"),
    ("Преподаватель", "Евдошенко Олег Игоревич"),
    ("Студент", "Кабанов Арсений, группа ЭФБО-17-25 (Вариант 1)"),
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

# Функция для вставки аккуратного моноширинного блока кода строго по левому краю
def insert_code_block(p, caption_text, code_text):
    # Оформляем параграф заголовка листинга
    p.text = caption_text
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.left_indent = Pt(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run_cap = p.runs[0]
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(11)
    run_cap.font.bold = True
    run_cap.font.color.rgb = RGBColor(15, 23, 42)

    # 1x1 таблица-карточка для моноширинного кода
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    p._element.addnext(tbl._element)

    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)

    # Фон и рамка карточки кода
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    cell._element.get_or_add_tcPr().append(shading)
    borders = parse_xml(f'''<w:tcBorders {nsdecls("w")}>
        <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
    </w:tcBorders>''')
    cell._element.get_or_add_tcPr().append(borders)

    mar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
        <w:top w:w="120" w:type="dxa"/>
        <w:bottom w:w="120" w:type="dxa"/>
        <w:left w:w="160" w:type="dxa"/>
        <w:right w:w="160" w:type="dxa"/>
    </w:tcMar>''')
    cell._element.get_or_add_tcPr().append(mar)

    # Каждая строка кода добавляется отдельным абзацем без отступов и выравнивания по ширине
    code_p = cell.paragraphs[0]
    lines = code_text.strip().split('\n')
    for idx, line in enumerate(lines):
        curr_p = code_p if idx == 0 else cell.add_paragraph()
        curr_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        curr_p.paragraph_format.first_line_indent = Pt(0)
        curr_p.paragraph_format.left_indent = Pt(0)
        curr_p.paragraph_format.line_spacing = 1.05
        curr_p.paragraph_format.space_before = Pt(0)
        curr_p.paragraph_format.space_after = Pt(0)
        
        r = curr_p.add_run(line if line else ' ')
        r.font.name = 'Consolas'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(15, 23, 42)

    return tbl

# Листинги кода для заданий 1-4
listing1_code = """// src/components/TaskList.jsx: условный вывод списка и итерация .map
import TaskItem from './TaskItem.jsx';

export default function TaskList({ tasks, categories, onToggle, onEdit, onDelete }) {
  const categoryNames = new Map(categories.map((cat) => [cat.id, cat.name]));

  return (
    <section aria-label="Список задач">
      <h2>Задачи (найдено: {tasks.length})</h2>
      {tasks.length === 0 ? (
        <p>Список задач пуст</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              categoryName={categoryNames.get(task.categoryId) ?? 'Без категории'}
              onToggle={onToggle}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

// src/App.jsx: состояние useState и вычисление отфильтрованного массива задач
import { useState } from 'react';
import { tasks as initialTasks, categories } from './data.js';
import { selectTasks } from './domain/task-service.js';

export default function App() {
  const [tasks, setTasks] = useState(() => initialTasks.map((t) => ({ ...t })));
  const [filters, setFilters] = useState({ q: '', completed: 'true', priority: '', categoryId: '' });

  // Вычисление отфильтрованных задач без дублирования состояний
  const visibleTasks = selectTasks(tasks, filters);
  // ..."""

listing2_code = """import { useEffect, useRef, useState } from 'react';

// Кастомный хук синхронизации состояния React с HTTP API (ПР8)
export function useTaskData({ api, filters }) {
  const [snapshot, setSnapshot] = useState({ tasks: [], categories: [], meta: { total: 0 } });
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);
  const [revision, setRevision] = useState(0);

  const mountedRef = useRef(false);
  const { q = '', completed = '', priority = '', categoryId = '' } = filters ?? {};

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  // Загрузка данных с управлением асинхронными флагами и отменой устаревших запросов
  useEffect(() => {
    let active = true;
    const controller = new AbortController();

    setStatus('loading');
    setError(null);

    async function load() {
      try {
        const nextSnapshot = await api.loadInitialData(
          { q, completed, priority, categoryId },
          { signal: controller.signal }
        );
        if (!active || !mountedRef.current) return;
        setSnapshot(nextSnapshot);
        setStatus('ready');
        setError(null);
      } catch (err) {
        if (!active || !mountedRef.current || controller.signal.aborted) return;
        setError(err);
        setStatus('error');
      }
    }

    void load();

    return () => {
      active = false;
      controller.abort();
    };
  }, [api, q, completed, priority, categoryId, revision]);

  const tasks = snapshot.tasks;
  const isLoading = status === 'loading';

  // Логирование переключения асинхронных состояний в консоль DevTools
  console.log(`[useTaskData] isLoading: ${isLoading}, tasks.length: ${tasks.length}`);

  return {
    snapshot,
    tasks,
    isLoading,
    error,
    refresh() {
      setRevision((prev) => prev + 1);
    },
  };
}"""

listing3_code = """// src/routes.js: серверная обработка маршрута GET и чтение параметров строки запроса
import { Router } from 'express';
import { parseFilters } from './validation.js';

export function createRouter(store) {
  const router = Router({ caseSensitive: true });

  // Серверный перехват GET /api/tasks с обработкой query-параметров фильтрации
  router.get('/tasks', (req, res) => {
    const searchParams = new URL(req.originalUrl, 'http://localhost').searchParams;
    const filters = parseFilters(searchParams);
    const data = store.listTasks(filters);
    res.status(200).json({ data, meta: { total: data.length, filters } });
  });

  return router;
}

// src/task-service.js: серверная фильтрация по признаку completed
export function selectTasks(tasks, filters = {}) {
  const { completed = null } = filters;
  if (completed === null) return [...tasks];
  return tasks.filter((task) => task.completed === completed);
}"""

listing4_code = """// src/task-validation.js: валидация входящего draft-объекта задачи
import { ApiError } from './errors.js';

export function validateTaskInput(value, { partial = false } = {}) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new ApiError(400, 'VALIDATION_ERROR', 'Тело запроса должно быть JSON-объектом.');
  }

  const details = Object.create(null);

  // Проверка обязательного поля названия: непустая строка после trim()
  if (!partial && !Object.hasOwn(value, 'title')) {
    details.title = 'Название обязательно.';
  } else if (Object.hasOwn(value, 'title')) {
    if (typeof value.title !== 'string') {
      details.title = 'Название должно быть строкой.';
    } else {
      const trimmed = value.title.trim();
      if (trimmed.length < 1 || trimmed.length > 100) {
        details.title = 'Длина названия должна быть от 1 до 100 символов.';
      }
    }
  }

  // При наличии ошибок выбрасываем исключение со статусом 400 Bad Request
  if (Object.keys(details).length > 0) {
    throw new ApiError(400, 'VALIDATION_ERROR', 'Ошибка валидации входящих данных задачи.', details);
  }

  return { title: value.title.trim(), priority: value.priority, categoryId: value.categoryId };
}

// src/routes.js: регистрация маршрута с централизованным перехватом ошибок
router.post('/tasks', express.json(), (req, res, next) => {
  try {
    const draft = validateTaskInput(req.body);
    const created = store.createTask(draft);
    res.status(201).json({ data: created });
  } catch (err) {
    next(err); // errorHandler отправляет клиенту статус 400 и структурированный JSON
  }
});"""

explanation4_text = "Пояснение. Клиентская валидация (атрибуты HTML5 required, minlength, обработчики onSubmit) выполняется в среде браузера пользователя и легко обходится прямыми HTTP-запросами через cURL, Postman или сторонние клиенты. Сервер является границей доверия (trust boundary), поэтому валидация на бэкенде критически обязательна для предотвращения порчи данных в хранилище, защиты от аномалий и сохранения целостности контракта API."

for p in doc.paragraphs:
    if "[Вставьте React-код: условный вывод списка и логику его фильтрации]" in p.text:
        insert_code_block(p, "Листинг 1. Реализация условного вывода списка и клиентской фильтрации:", listing1_code)

    elif "[Покажите экран приложения с работающим фильтром «Завершенные»]" in p.text:
        p.text = "Скриншот 1. Интерфейс приложения с активным фильтром «Завершенные» (кнопка активна, в списке только выполненные задачи):"
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run_shot = p.runs[0]
        run_shot.font.name = "Times New Roman"
        run_shot.font.size = Pt(11)
        run_shot.font.bold = True
        
        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(4)
        img_p.paragraph_format.space_after = Pt(10)
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot1.png"), width=Inches(5.8))
        
    elif "[Вставьте код кастомного хука useTaskData]" in p.text:
        insert_code_block(p, "Листинг 2. Кастомный асинхронный хук useTaskData с управлением состояниями:", listing2_code)

    elif "[Покажите логи последовательной смены isLoading и данных в консоли DevTools]" in p.text:
        p.text = "Скриншот 2. Логирование пошаговой смены асинхронных состояний (isLoading: true -> false, tasks: 0 -> 12) в консоли браузера:"
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run_shot = p.runs[0]
        run_shot.font.name = "Times New Roman"
        run_shot.font.size = Pt(11)
        run_shot.font.bold = True

        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(4)
        img_p.paragraph_format.space_after = Pt(10)
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot2.png"), width=Inches(5.8))

    elif "[Вставьте серверный код обработки маршрута GET и чтения параметров строки запроса]" in p.text:
        insert_code_block(p, "Листинг 3. Серверная обработка маршрута GET /api/tasks с извлечением query-параметров:", listing3_code)

    elif "[Покажите отфильтрованный JSON-ответ сервера и HTTP-статус 200]" in p.text:
        p.text = "Скриншот 3. Ответ сервера по запросу GET /api/tasks?completed=true со статусом 200 OK и отфильтрованным JSON-массивом:"
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run_shot = p.runs[0]
        run_shot.font.name = "Times New Roman"
        run_shot.font.size = Pt(11)
        run_shot.font.bold = True

        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(4)
        img_p.paragraph_format.space_after = Pt(10)
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot3.png"), width=Inches(5.8))

    elif "[Вставьте код валидации POST-запроса и отправки статус-кода 400]" in p.text:
        insert_code_block(p, "Листинг 4. Модуль серверной валидации POST-запроса и отправка ошибки 400 Bad Request:", listing4_code)

    elif "[Покажите статус 400 Bad Request и JSON-текст ошибки от сервера]" in p.text:
        p.text = "Скриншот 4. Ответ сервера со статусом 400 Bad Request и структурированной ошибкой в JSON на невалидный POST-запрос:"
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Pt(0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        run_shot = p.runs[0]
        run_shot.font.name = "Times New Roman"
        run_shot.font.size = Pt(11)
        run_shot.font.bold = True

        img_p = doc.add_paragraph()
        p._element.addnext(img_p._element)
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(4)
        img_p.paragraph_format.space_after = Pt(8)
        img_p.add_run().add_picture(os.path.join(screenshots_dir, "screenshot4.png"), width=Inches(5.8))
        
        # Добавляем пояснение, запрашиваемое заданием 4
        p_exp = doc.add_paragraph()
        img_p._element.addnext(p_exp._element)
        p_exp.text = explanation4_text
        p_exp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_exp.paragraph_format.first_line_indent = Pt(18)
        p_exp.paragraph_format.space_before = Pt(4)
        p_exp.paragraph_format.space_after = Pt(8)
        p_exp.runs[0].font.name = "Times New Roman"
        p_exp.runs[0].font.size = Pt(11)

doc.save(output_path)
print("Saved beautifully formatted report to:", output_path, "Size:", os.path.getsize(output_path), "bytes")
