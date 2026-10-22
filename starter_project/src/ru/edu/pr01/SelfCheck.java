package ru.edu.pr01;

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

    public static void main(String[] args) {
        // Проверки базовой стоимости
        check("base/typical", () -> OrderCalculator.calculateBase(2, 100.0) == 200.0);
        check("base/zero_qty", () -> OrderCalculator.calculateBase(0, 100.0) == 0.0);

        // Проверки расчета скидки
        check("discount/typical", () -> OrderCalculator.applyDiscount(200.0, 10.0) == 180.0);
        check("discount/zero", () -> OrderCalculator.applyDiscount(200.0, 0.0) == 200.0);
        check("discount/max", () -> OrderCalculator.applyDiscount(100.0, 30.0) == 70.0);

        // Проверки расчета НДС (Вариант 4: 25%)
        check("vat/variant4_rate", () -> OrderCalculator.VAT_RATE == 25.0);
        check("vat/typical", () -> Math.abs(OrderCalculator.calculateVat(180.0, 25.0) - 45.0) < 0.001);

        // Проверки итоговой стоимости
        check("total/reference_test", () -> Math.abs(OrderCalculator.calculateTotal(2, 100.0, 10.0, 20.0) - 216.0) < 0.001);
        check("total/variant4_typical", () -> Math.abs(OrderCalculator.calculateTotal(2, 100.0, 10.0, OrderCalculator.VAT_RATE) - 225.0) < 0.001);
        check("total/zero_discount", () -> Math.abs(OrderCalculator.calculateTotal(2, 100.0, 0.0, OrderCalculator.VAT_RATE) - 250.0) < 0.001);

        // Проверки валидации входных параметров и границ
        check("isValid/typical", () -> OrderCalculator.isValid(12, 2490.50, 5.0));
        check("isValid/lower_bound", () -> OrderCalculator.isValid(1, 0.01, 0.0));
        check("isValid/upper_bound", () -> OrderCalculator.isValid(10000, 5000000.0, 30.0));
        check("isValid/invalid_qty_zero", () -> !OrderCalculator.isValid(0, 1000.0, 10.0));
        check("isValid/invalid_qty_negative", () -> !OrderCalculator.isValid(-1, 100.0, 0.0));
        check("isValid/invalid_qty_overflow", () -> !OrderCalculator.isValid(10001, 100.0, 0.0));
        check("isValid/invalid_price_zero", () -> !OrderCalculator.isValid(5, 0.0, 5.0));
        check("isValid/invalid_price_negative", () -> !OrderCalculator.isValid(5, -20.0, 5.0));
        check("isValid/invalid_price_overflow", () -> !OrderCalculator.isValid(1, 5000001.0, 0.0));
        check("isValid/invalid_discount_negative", () -> !OrderCalculator.isValid(3, 100.0, -1.0));
        check("isValid/invalid_discount_over_limit", () -> !OrderCalculator.isValid(3, 999.99, 35.0));

        System.out.println();
        System.out.println("ИТОГО: Пройдено " + passed + " из " + (passed + failed));
        if (failed == 0) {
            System.out.println("PASS");
        } else {
            System.out.println("FAIL");
        }
    }
}
