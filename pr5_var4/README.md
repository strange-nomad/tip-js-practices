# Практическая работа №5: Анализ табеля рабочего времени (TimesheetAnalyzer)

Учебный проект по дисциплине «Информационные системы в бизнесе» (РТУ МИРЭА).

## Автор
- **Студент:** Кабанов Арсений
- **Группа:** ЭФБО-17-25
- **Вариант:** №4 (Часть А: `total` без нулей; Часть Б: `addWorkingDaysCount`)

## Структура проекта
```text
pr5_var4/
├── data/
│   └── sample.csv                   # Тестовые наборы данных (data-driven тесты)
├── diagrams/
│   ├── activity_partial.dot/.png    # Исходная Activity-диаграмма с TODO
│   ├── activity_completed.dot/.png  # Дополненная Activity-диаграмма (Вариант 4)
│   ├── class_partial.dot/.png       # Исходная диаграмма классов
│   └── class_completed.dot/.png     # Дополненная диаграмма классов (Вариант 4)
├── src/
│   └── ru/
│       └── edu/
│           └── pr02/
│               ├── TimesheetAnalyzer.java # Модуль анализа табеля и валидации R1-R9
│               └── SelfCheck.java         # Автономный тест-раннер (23 unit-теста + CSV)
├── .gitignore                       # Исключения сборки
├── DECISIONS.md                     # Обоснование архитектурных решений
├── README.md                        # Описание и запуск
├── run_selfcheck.bat                # Скрипт сборки и тестирования для Windows
└── run_selfcheck.sh                 # Скрипт сборки и тестирования для Linux/macOS
```

## Инструкция по запуску

### Запуск через готовый скрипт:
- **Windows:** `run_selfcheck.bat`
- **Linux/macOS:** `./run_selfcheck.sh`

### Ручной запуск:
```bash
javac -encoding UTF-8 -d out src/ru/edu/pr02/*.java
java -cp out ru.edu.pr02.SelfCheck
```

### Запуск анализатора для конкретной строки:
```bash
java -cp out ru.edu.pr02.TimesheetAnalyzer "8;8;9;10;8"
```
