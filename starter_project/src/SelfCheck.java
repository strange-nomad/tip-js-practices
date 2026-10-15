package starter_project;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.util.Locale;

/**
 * Модуль автоматической самопроверки и граничного тестирования расчётного ядра.
 * Выполняет верификацию бизнес-правил и чтение открытого набора sample.csv.
 */
public class SelfCheck {

    private static int testsRun = 0;
    private static int testsPassed = 0;

    public static void main(String[] args) {
        System.out.println("==========================================================");
        System.out.println("  ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ И ГРАНИЧНЫХ ПРОВЕРОК");
        System.out.println("==========================================================");

        // 1. Проверка типового корректного сценария
        testNormalCalculation();

        // 2. Проверка нижней границы диапазонов (quantity=1, price=0.01, discount=0.0)
        testLowerBoundary();

        // 3. Проверка верхней границы диапазонов (quantity=10000, price=5000000.0, discount=30.0)
        testUpperBoundary();

        // 4. Проверка выхода за нижнюю границу (quantity=0, price=0.0, discount=-1.0)
        testBelowLowerBoundary();

        // 5. Проверка выхода за верхнюю границу (quantity=10001, price=5000000.01, discount=30.1)
        testAboveUpperBoundary();

        // 6. Проверка независимости применения скидки и начисления НДС
        testVatFormulaAfterDiscount();

        // 7. Прогон набора данных из sample.csv
        testCsvSuite();

        System.out.println("\n==========================================================");
        System.out.printf("ИТОГ ТЕСТИРОВАНИЯ: Пройдено %d из %d проверок (%s)\n",
                testsPassed, testsRun, (testsPassed == testsRun ? "ВСЕ ТЕСТЫ УСПЕШНЫ" : "ЕСТЬ ОШИБКИ"));
        System.out.println("==========================================================");
    }

    private static void assertTrue(String testName, boolean condition) {
        testsRun++;
        if (condition) {
            testsPassed++;
            System.out.printf(Locale.US, "  [PASS] %-60s\n", testName);
        } else {
            System.out.printf(Locale.US, "  [FAIL] %-60s <-- ОШИБКА!\n", testName);
        }
    }

    private static void testNormalCalculation() {
        int qty = 10;
        double price = 1000.0;
        double discount = 10.0;

        boolean valid = OrderCalculator.isValid(qty, price, discount);
        double base = OrderCalculator.calculateBase(qty, price);
        double discAmt = OrderCalculator.calculateDiscountAmount(base, discount);
        double discounted = OrderCalculator.applyDiscount(base, discount);
        double vat = OrderCalculator.calculateVat(discounted, OrderCalculator.VAT_RATE);
        double total = discounted + vat;

        assertTrue("Типовой расчёт: валидность входных данных", valid);
        assertTrue("Типовой расчёт: базовая сумма 10 * 1000 = 10 000.00", Math.abs(base - 10000.0) < 0.001);
        assertTrue("Типовой расчёт: скидка 10% = 1000.00", Math.abs(discAmt - 1000.0) < 0.001);
        assertTrue("Типовой расчёт: сумма со скидкой = 9 000.00", Math.abs(discounted - 9000.0) < 0.001);
        assertTrue("Типовой расчёт: НДС 25% от 9 000 = 2 250.00", Math.abs(vat - 2250.0) < 0.001);
        assertTrue("Типовой расчёт: итого к оплате = 11 250.00", Math.abs(total - 11250.0) < 0.001);
    }

    private static void testLowerBoundary() {
        int qty = 1;
        double price = 0.01;
        double discount = 0.0;

        boolean valid = OrderCalculator.isValid(qty, price, discount);
        double base = OrderCalculator.calculateBase(qty, price);
        double discounted = OrderCalculator.applyDiscount(base, discount);
        double vat = OrderCalculator.calculateVat(discounted, OrderCalculator.VAT_RATE);
        double total = discounted + vat;

        assertTrue("Нижняя граница: количество 1, цена 0.01, скидка 0%", valid);
        assertTrue("Нижняя граница: базовая сумма 0.01 руб.", Math.abs(base - 0.01) < 0.0001);
        assertTrue("Нижняя граница: итого 0.0125 руб.", Math.abs(total - 0.0125) < 0.0001);
    }

    private static void testUpperBoundary() {
        int qty = 10_000;
        double price = 5_000_000.0;
        double discount = 30.0;

        boolean valid = OrderCalculator.isValid(qty, price, discount);
        double base = OrderCalculator.calculateBase(qty, price);
        double discounted = OrderCalculator.applyDiscount(base, discount);
        double vat = OrderCalculator.calculateVat(discounted, OrderCalculator.VAT_RATE);
        double total = discounted + vat;

        assertTrue("Верхняя граница: количество 10000, цена 5 000 000, скидка 30%", valid);
        assertTrue("Верхняя граница: базовая сумма 50 000 000 000", Math.abs(base - 50_000_000_000.0) < 1.0);
        assertTrue("Верхняя граница: стоимость со скидкой 35 000 000 000", Math.abs(discounted - 35_000_000_000.0) < 1.0);
        assertTrue("Верхняя граница: НДС 25% = 8 750 000 000", Math.abs(vat - 8_750_000_000.0) < 1.0);
        assertTrue("Верхняя граница: итого 43 750 000 000", Math.abs(total - 43_750_000_000.0) < 1.0);
    }

    private static void testBelowLowerBoundary() {
        assertTrue("Отказ: количество 0 недопустимо", !OrderCalculator.isValid(0, 100.0, 5.0));
        assertTrue("Отказ: отрицательное количество недопустимо", !OrderCalculator.isValid(-5, 100.0, 5.0));
        assertTrue("Отказ: цена 0.0 недопустима", !OrderCalculator.isValid(10, 0.0, 5.0));
        assertTrue("Отказ: отрицательная цена недопустима", !OrderCalculator.isValid(10, -100.0, 5.0));
        assertTrue("Отказ: отрицательная скидка недопустима", !OrderCalculator.isValid(10, 100.0, -1.0));
    }

    private static void testAboveUpperBoundary() {
        assertTrue("Отказ: количество 10 001 превышает максимум", !OrderCalculator.isValid(10_001, 100.0, 5.0));
        assertTrue("Отказ: цена 5 000 000.01 превышает максимум", !OrderCalculator.isValid(10, 5_000_000.01, 5.0));
        assertTrue("Отказ: скидка 30.1% превышает максимум", !OrderCalculator.isValid(10, 100.0, 30.1));
    }

    private static void testVatFormulaAfterDiscount() {
        // Проверка правила: НДС начисляется строго ПОСЛЕ скидки
        double base = 1000.0;
        double discount = 20.0; // сумма со скидкой = 800
        double discounted = OrderCalculator.applyDiscount(base, discount);
        double vat = OrderCalculator.calculateVat(discounted, OrderCalculator.VAT_RATE); // 800 * 0.25 = 200

        // Ошибочный расчет (до скидки): 1000 * 0.25 = 250
        double wrongVat = base * OrderCalculator.VAT_RATE;

        assertTrue("Правило ЖЦ: НДС равен 200.00, а не 250.00", Math.abs(vat - 200.0) < 0.001);
        assertTrue("Различие правильного и ошибочного НДС составляет 50.00 руб.", Math.abs(wrongVat - vat - 50.0) < 0.001);
    }

    private static void testCsvSuite() {
        File csvFile = new File("starter_project/data/sample.csv");
        if (!csvFile.exists()) {
            csvFile = new File("data/sample.csv");
        }
        if (!csvFile.exists()) {
            System.out.println("  [SKIP] Файл sample.csv не найден, пропускаем пакетный тест.");
            return;
        }

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            String line = br.readLine(); // Пропуск заголовка
            int lineCount = 0;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) continue;
                String[] parts = line.split(",");
                if (parts.length < 5) continue;

                int qty = Integer.parseInt(parts[1].trim());
                double price = Double.parseDouble(parts[2].trim());
                double discount = Double.parseDouble(parts[3].trim());
                boolean expectedValid = Boolean.parseBoolean(parts[4].trim());

                boolean actualValid = OrderCalculator.isValid(qty, price, discount);
                assertTrue(String.format(Locale.US, "CSV Строка %d (%s): ожидание %b",
                        ++lineCount, parts[0], expectedValid), actualValid == expectedValid);
            }
        } catch (Exception e) {
            System.out.println("  [ERROR] Ошибка чтения CSV: " + e.getMessage());
        }
    }
}
