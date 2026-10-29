package ru.edu.pr03;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

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

    private static boolean expectException(Runnable runnable) {
        try {
            runnable.run();
            return false;
        } catch (IllegalArgumentException e) {
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public static void main(String[] args) {
        System.out.println("Запуск проверок SelfCheck (ПР №6, Вариант 4)...");
        ApprovalRouter router = new ApprovalRouter();

        // 1. Проверки приоритетов правил и пересечений (R1-R4)
        check("intersect/personal_over_urgent", () -> router.route(10_000L, true, RiskLevel.LOW, true) == ApprovalRoute.SECURITY_REVIEW);
        check("intersect/high_over_urgent", () -> router.route(10_000L, true, RiskLevel.HIGH, false) == ApprovalRoute.DIRECTOR_REVIEW);
        check("intersect/personal_over_high", () -> router.route(10_000L, false, RiskLevel.HIGH, true) == ApprovalRoute.SECURITY_REVIEW);
        check("intersect/amount_over_urgent", () -> router.route(600_000L, true, RiskLevel.LOW, false) == ApprovalRoute.FINANCE_REVIEW);

        // 2. Базовые сценарии маршрутизации
        check("basic/fast_track", () -> router.route(10_000L, true, RiskLevel.LOW, false) == ApprovalRoute.FAST_TRACK);
        check("basic/finance_limit", () -> router.route(500_000L, false, RiskLevel.LOW, false) == ApprovalRoute.FINANCE_REVIEW);
        check("basic/standard_small", () -> router.route(10_000L, false, RiskLevel.LOW, false) == ApprovalRoute.STANDARD);
        check("basic/security_review", () -> router.route(10_000L, false, RiskLevel.LOW, true) == ApprovalRoute.SECURITY_REVIEW);

        // 3. Граничные значения вокруг FINANCE_LIMIT (500 000)
        check("bound/fast_track_499999", () -> router.route(499_999L, true, RiskLevel.LOW, false) == ApprovalRoute.FAST_TRACK);
        check("bound/finance_500001", () -> router.route(500_001L, false, RiskLevel.LOW, false) == ApprovalRoute.FINANCE_REVIEW);

        // 4. Защитные условия (контракты параметров)
        check("defensive/amount_negative", () -> expectException(() -> router.route(-1L, true, RiskLevel.LOW, false)));
        check("defensive/risk_null", () -> expectException(() -> router.route(10_000L, true, null, false)));

        // 5. Проверки Варианта 4, Часть А (ужесточение правила R5 STANDARD)
        check("var4/standard_under_50k", () -> router.route(49_999L, false, RiskLevel.LOW, false) == ApprovalRoute.STANDARD);
        check("var4/escalate_finance_50k", () -> router.route(50_000L, false, RiskLevel.LOW, false) == ApprovalRoute.FINANCE_REVIEW);
        check("var4/escalate_finance_100k", () -> router.route(100_000L, false, RiskLevel.LOW, false) == ApprovalRoute.FINANCE_REVIEW);
        check("var4/escalate_medium_risk", () -> router.route(10_000L, false, RiskLevel.MEDIUM, false) == ApprovalRoute.DIRECTOR_REVIEW);

        // 6. Проверки Варианта 4, Часть Б (метод addStandardEligibility)
        check("var4_eligibility/eligible", () -> router.addStandardEligibility(10_000L, false, RiskLevel.LOW, false));
        check("var4_eligibility/exceed_amount", () -> !router.addStandardEligibility(50_000L, false, RiskLevel.LOW, false));
        check("var4_eligibility/urgent_flag", () -> !router.addStandardEligibility(10_000L, true, RiskLevel.LOW, false));
        check("var4_eligibility/medium_risk", () -> !router.addStandardEligibility(10_000L, false, RiskLevel.MEDIUM, false));
        check("var4_eligibility/has_personal", () -> !router.addStandardEligibility(10_000L, false, RiskLevel.LOW, true));

        // 7. Data-driven тестирование по data/sample.csv
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

    private static void runDataDrivenTests(String csvPath) {
        File file = new File(csvPath);
        if (!file.exists()) {
            return;
        }

        ApprovalRouter router = new ApprovalRouter();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int lineNum = 0;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#") || line.startsWith("amount;")) {
                    continue;
                }

                lineNum++;
                final String currentLine = line;
                final int currentLineNum = lineNum;

                check("data_driven/case_" + currentLineNum, () -> {
                    String[] parts = currentLine.split(";", -1);
                    if (parts.length < 5) {
                        return false;
                    }

                    long amount = Long.parseLong(parts[0]);
                    boolean urgent = Boolean.parseBoolean(parts[1]);
                    String riskStr = parts[2];
                    boolean personal = Boolean.parseBoolean(parts[3]);
                    String expected = parts[4];

                    RiskLevel risk = riskStr.equalsIgnoreCase("null") ? null : RiskLevel.valueOf(riskStr);

                    if (expected.equals("ERROR")) {
                        return expectException(() -> router.route(amount, urgent, risk, personal));
                    } else {
                        ApprovalRoute expRoute = ApprovalRoute.valueOf(expected);
                        ApprovalRoute actual = router.route(amount, urgent, risk, personal);
                        return actual == expRoute;
                    }
                });
            }
        } catch (Exception e) {
            System.out.println("[FAIL] data_driven (Ошибка чтения CSV: " + e.getMessage() + ")");
            failed++;
        }
    }
}
