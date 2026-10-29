# Практическая работа №6: Маршрутизация заявок (ApprovalRouter)

Учебный проект по дисциплине «Информационные системы в бизнесе» (РТУ МИРЭА).

## Автор
- **Студент:** Кабанов Арсений
- **Группа:** ЭФБО-17-25
- **Вариант:** №4 (Часть А: ужесточение `STANDARD`; Часть Б: метод `addStandardEligibility`)

## Структура проекта
```text
pr6_var4/
├── data/
│   └── sample.csv                   # Контрольные наборы данных (data-driven тесты)
├── diagrams/
│   ├── activity_partial.dot/.png    # Исходная Activity-диаграмма
│   ├── activity_completed.dot/.png  # Дополненная Activity-диаграмма (Вариант 4)
│   ├── class_partial.dot/.png       # Исходная диаграмма классов
│   └── class_completed.dot/.png     # Дополненная диаграмма классов (Вариант 4)
├── src/
│   └── ru/
│       └── edu/
│           └── pr03/
│               ├── ApprovalRoute.java   # enum маршрутов согласования
│               ├── RiskLevel.java       # enum уровней риска
│               ├── ApprovalRouter.java  # Логика маршрутизации и валидации
│               └── SelfCheck.java       # Тестовый раннер (20 unit-тестов + CSV)
├── .gitignore                       # Исключения сборки
├── DECISIONS.md                     # Обоснование архитектурных решений
├── README.md                        # Описание и запуск
├── run_selfcheck.bat                # Скрипт сборки и тестирования для Windows
└── run_selfcheck.sh                 # Скрипт сборки и тестирования для Linux/macOS
```

## Инструкция по запуску

### Запуск тестов через скрипт:
- **Windows:** `run_selfcheck.bat`
- **Linux/macOS:** `./run_selfcheck.sh`

### Ручной запуск:
```bash
javac -encoding UTF-8 -d out src/ru/edu/pr03/*.java
java -cp out ru.edu.pr03.SelfCheck
```
