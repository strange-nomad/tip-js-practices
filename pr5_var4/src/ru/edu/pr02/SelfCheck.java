package ru.edu.pr02;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Arrays;

public class SelfCheck {

    @FunctionalInterface
    interface CheckFunction {
        boolean run() throws Exception;
    }

    private static int passed = 0;
    private static int failed = 0;

    private static void check(String name, CheckFunction test) {
        try {
            if (test.run()) {
                System.out.println("[PASS] " + name);
                passed++;
            } else {
                System.out.println("[FAIL] " + name);
                failed++;
            }
        } catch (Exception e) {
            System.out.println("[FAIL] " + name + " (Исключение: " + e.getMessage() + ")");
            failed++;
        }
    }

    // Проверка ожидаемого исключения и вхождения подстроки в сообщение
    private static boolean expectException(Runnable runnable, String messageSubstring) {
        try {
            runnable.run();
            return false;
        } catch (IllegalArgumentException e) {
            return messageSubstring == null || e.getMessage().toLowerCase().contains(messageSubstring.toLowerCase());
        } catch (Exception e) {
            return false;
        }
    }

    public static void main(String[] args) {
        System.out.println("Запуск модульных проверок SelfCheck (ПР №5, Вариант 4)...");

        // 1. Проверки разбора строки parseHours (R1-R9)
        check("parseHours/valid", () -> Arrays.equals(TimesheetAnalyzer.parseHours("8;9;10;8;8"), new int[]{8, 9, 10, 8, 8}));
        check("parseHours/empty", () -> expectException(() -> TimesheetAnalyzer.parseHours(""), "структура"));
        check("parseHours/out_of_range", () -> expectException(() -> TimesheetAnalyzer.parseHours("8;8;17;8;8"), "позиция 3"));
        check("parseHours/not_number", () -> expectException(() -> TimesheetAnalyzer.parseHours("8;abc;8;8;8"), "позиция 2"));
        check("parseHours/four_values", () -> expectException(() -> TimesheetAnalyzer.parseHours("8;8;8;8"), "структура"));
        check("parseHours/trailing_semicolon", () -> expectException(() -> TimesheetAnalyzer.parseHours("8;8;8;8;8;"), "структура"));
        check("parseHours/leading_zero", () -> expectException(() -> TimesheetAnalyzer.parseHours("08;8;8;8;8"), "позиция 1"));

        // 2. Проверки базового суммирования total
        check("total/typical", () -> TimesheetAnalyzer.total(new int[]{8, 9, 10, 8, 8}) == 43);
        check("total/lower_bound", () -> TimesheetAnalyzer.total(new int[]{0, 0, 0, 0, 0}) == 0);
        check("total/upper_bound", () -> TimesheetAnalyzer.total(new int[]{16, 16, 16, 16, 16}) == 80);

        // 3. Проверки среднего значения average
        check("average/typical", () -> Math.abs(TimesheetAnalyzer.average(new int[]{8, 9, 10, 8, 8}) - 8.60) < 0.001);
        check("average/integer", () -> Math.abs(TimesheetAnalyzer.average(new int[]{8, 8, 8, 8, 8}) - 8.00) < 0.001);
        check("average/fractional", () -> Math.abs(TimesheetAnalyzer.average(new int[]{7, 8, 9, 8, 7}) - 7.80) < 0.001);

        // 4. Проверки количества дней переработки overtimeDays
        check("overtimeDays/zero", () -> TimesheetAnalyzer.overtimeDays(new int[]{8, 8, 8, 8, 8}) == 0);
        check("overtimeDays/two_days", () -> TimesheetAnalyzer.overtimeDays(new int[]{9, 8, 7, 10, 8}) == 2);
        check("overtimeDays/boundary_eight", () -> TimesheetAnalyzer.overtimeDays(new int[]{8, 9, 8, 8, 8}) == 1);

        // 5. Проверки недельной переработки weeklyOvertime
        check("weeklyOvertime/forty", () -> TimesheetAnalyzer.weeklyOvertime(new int[]{8, 8, 8, 8, 8}) == 0);
        check("weeklyOvertime/fifty", () -> TimesheetAnalyzer.weeklyOvertime(new int[]{10, 10, 10, 10, 10}) == 10);
        check("weeklyOvertime/under_forty", () -> TimesheetAnalyzer.weeklyOvertime(new int[]{6, 6, 6, 6, 6}) == 0);

        // 6. Проверки индивидуального Варианта 4 (Часть А: total исключает нули)
        check("var4_total/exclude_zeros", () -> TimesheetAnalyzer.total(new int[]{8, 0, 10, 0, 8}) == 26);
        check("var4_total/all_zeros", () -> TimesheetAnalyzer.total(new int[]{0, 0, 0, 0, 0}) == 0);

        // 7. Проверки индивидуального Варианта 4 (Часть Б: addWorkingDaysCount)
        check("var4_workingDays/mixed", () -> TimesheetAnalyzer.addWorkingDaysCount(new int[]{8, 0, 10, 0, 8}) == 3);
        check("var4_workingDays/all_worked", () -> TimesheetAnalyzer.addWorkingDaysCount(new int[]{8, 8, 8, 8, 8}) == 5);
        check("var4_workingDays/all_vacation", () -> TimesheetAnalyzer.addWorkingDaysCount(new int[]{0, 0, 0, 0, 0}) == 0);

        // 8. Data-driven тестирование по файлу sample.csv
        runDataDrivenTests("data/sample.csv");

        System.out.println();
        System.out.println("ИТОГО: Пройдено " + passed + " из " + (passed + failed));
        if (failed == 0) {
            System.out.println("PASS");
        } else {
            System.out.println("FAIL");
            System.exit(1);
        }
    }

    // Прогон тестов из CSV файла
    private static void runDataDrivenTests(String csvPath) {
        File file = new File(csvPath);
        if (!file.exists()) {
            return;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int lineNum = 0;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue;
                }

                lineNum++;
                final String currentLine = line;
                final int currentLineNum = lineNum;

                check("data_driven/case_" + currentLineNum, () -> {
                    String[] parts = currentLine.split("\\|", -1);
                    if (parts.length < 2) {
                        return false;
                    }
                    String input = parts[0].equals("EMPTY") ? "" : parts[0];
                    String expected = parts[1];

                    if (expected.startsWith("ERROR:")) {
                        String expectedSub = expected.substring("ERROR:".length());
                        return expectException(() -> TimesheetAnalyzer.parseHours(input), expectedSub);
                    } else if (expected.startsWith("OK:")) {
                        int[] hours = TimesheetAnalyzer.parseHours(input);
                        int total = TimesheetAnalyzer.total(hours);
                        double avg = TimesheetAnalyzer.average(hours);
                        int od = TimesheetAnalyzer.overtimeDays(hours);
                        int wo = TimesheetAnalyzer.weeklyOvertime(hours);

                        // Парсинг ожидаемых показателей
                        // Формат: OK:sum=40,avg=8.00,od=0,wo=0
                        String expParams = expected.substring("OK:".length());
                        String[] tokens = expParams.split(",");
                        int expSum = 0;
                        double expAvg = 0.0;
                        int expOd = 0;
                        int expWo = 0;
                        for (String tok : tokens) {
                            String[] kv = tok.split("=");
                            if (kv[0].equals("sum")) expSum = Integer.parseInt(kv[1]);
                            if (kv[0].equals("avg")) expAvg = Double.parseDouble(kv[1]);
                            if (kv[0].equals("od")) expOd = Integer.parseInt(kv[1]);
                            if (kv[0].equals("wo")) expWo = Integer.parseInt(kv[1]);
                        }

                        return total == expSum
                                && Math.abs(avg - expAvg) < 0.01
                                && od == expOd
                                && wo == expWo;
                    }
                    return false;
                });
            }
        } catch (Exception e) {
            System.out.println("[FAIL] data_driven (Ошибка чтения CSV: " + e.getMessage() + ")");
            failed++;
        }
    }
}
