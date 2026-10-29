package ru.edu.pr02;

public class TimesheetAnalyzer {

    // Обязательные константы модели
    public static final int DAYS_COUNT = 5;
    public static final int MIN_HOURS = 0;
    public static final int MAX_HOURS = 16;
    public static final int DAILY_NORM = 8;
    public static final int WEEKLY_NORM = 40;

    // Разбор строки табеля и валидация правил R1-R9
    public static int[] parseHours(String line) {
        if (line == null) {
            throw new IllegalArgumentException("Ошибка: строка табеля null");
        }

        // R1: строго ровно 5 значений при split с limit = -1
        String[] parts = line.split(";", -1);
        if (parts.length != DAYS_COUNT) {
            throw new IllegalArgumentException("Ошибка: структура -- ожидается ровно " + DAYS_COUNT + " значений, получено " + parts.length);
        }

        int[] hours = new int[DAYS_COUNT];

        // Позиции нумеруются с 1 (R8), стратегия fail-fast (R7)
        for (int i = 0; i < DAYS_COUNT; i++) {
            String p = parts[i];

            // R2, R9: проверка формата целого числа без знака и ведущих нулей
            if (!p.matches("^(0|[1-9][0-9]*)$")) {
                throw new IllegalArgumentException("Ошибка: позиция " + (i + 1) + " -- некорректный формат числа: '" + p + "'");
            }

            int val = Integer.parseInt(p);

            // R3: проверка диапазона допустимых часов
            if (val < MIN_HOURS || val > MAX_HOURS) {
                throw new IllegalArgumentException("Ошибка: позиция " + (i + 1) + " -- значение " + val + " вне диапазона [" + MIN_HOURS + ", " + MAX_HOURS + "]");
            }

            hours[i] = val;
        }

        return hours;
    }

    // Защитные проверки массива часов
    private static void validateHoursArray(int[] hours) {
        if (hours == null) {
            throw new IllegalArgumentException("Ошибка: массив часов null");
        }
        if (hours.length != DAYS_COUNT) {
            throw new IllegalArgumentException("Ошибка: некорректная длина массива часов: " + hours.length);
        }
    }

    // Суммарное количество часов за неделю
    // Вариант 4, Часть А: суммируются только ненулевые дни (выходные с 0 часов исключаются)
    public static int total(int[] hours) {
        validateHoursArray(hours);
        int sum = 0;
        for (int h : hours) {
            if (h > 0) {
                sum += h;
            }
        }
        return sum;
    }

    // Среднее количество часов в день с округлением до двух знаков
    public static double average(int[] hours) {
        validateHoursArray(hours);
        int sum = total(hours);
        double rawAvg = (double) sum / DAYS_COUNT;
        return Math.round(rawAvg * 100.0) / 100.0;
    }

    // Количество дней с переработкой (более 8 часов)
    public static int overtimeDays(int[] hours) {
        validateHoursArray(hours);
        int count = 0;
        for (int h : hours) {
            if (h > DAILY_NORM) {
                count++;
            }
        }
        return count;
    }

    // Недельная переработка сверх нормы 40 часов
    public static int weeklyOvertime(int[] hours) {
        validateHoursArray(hours);
        return Math.max(0, total(hours) - WEEKLY_NORM);
    }

    // Вариант 4, Часть Б: подсчет фактически отработанных дней (значение часов > 0)
    public static int addWorkingDaysCount(int[] hours) {
        validateHoursArray(hours);
        int workingDays = 0;
        for (int h : hours) {
            if (h > 0) {
                workingDays++;
            }
        }
        return workingDays;
    }

    // Консольный запуск для демонстрации
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Использование: java -cp out ru.edu.pr02.TimesheetAnalyzer \"8;8;9;10;8\"");
            return;
        }

        String input = args[0];
        try {
            int[] hours = parseHours(input);
            System.out.println("Сумма часов (Вариант 4, ненулевые): " + total(hours));
            System.out.printf("Среднее в день: %.2f\n", average(hours));
            System.out.println("Дней с переработкой (>8 ч): " + overtimeDays(hours));
            System.out.println("Недельная переработка (>40 ч): " + weeklyOvertime(hours));
            System.out.println("Отработано дней (Вариант 4, Часть Б): " + addWorkingDaysCount(hours));
        } catch (IllegalArgumentException e) {
            System.out.println("ОШИБКА: " + e.getMessage());
        }
    }
}
