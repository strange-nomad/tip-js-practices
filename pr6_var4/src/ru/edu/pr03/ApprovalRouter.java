package ru.edu.pr03;

public class ApprovalRouter {

    // Лимит для автоматического финансового согласования
    public static final long FINANCE_LIMIT = 500_000L;

    // Порог суммы для стандартного маршрута по Варианту 4
    public static final long STANDARD_LIMIT = 50_000L;

    // Выбор маршрута согласования служебной заявки по правилам R1-R5
    public ApprovalRoute route(long amount, boolean urgent, RiskLevel risk, boolean containsPersonalData) {
        // Защитные условия (контракты)
        if (amount < 0) {
            throw new IllegalArgumentException("amount must be >= 0, got " + amount);
        }
        if (risk == null) {
            throw new IllegalArgumentException("risk is null");
        }

        // R1: наивысший приоритет -- персональные данные требуют проверки безопасности
        if (containsPersonalData) {
            return ApprovalRoute.SECURITY_REVIEW;
        }

        // R2: высокий риск требует согласования директора
        if (risk == RiskLevel.HIGH) {
            return ApprovalRoute.DIRECTOR_REVIEW;
        }

        // R3: сумма от 500 000 руб. требует финансового согласования
        if (amount >= FINANCE_LIMIT) {
            return ApprovalRoute.FINANCE_REVIEW;
        }

        // R4: срочная заявка до 500 000 руб. направляется на ускоренный трек
        if (urgent) {
            return ApprovalRoute.FAST_TRACK;
        }

        // R5: Вариант 4 (Часть А): ужесточение стандартного маршрута
        // STANDARD применяется только если сумма < 50 000, риск LOW и заявка не срочная.
        // Иначе требуется DIRECTOR_REVIEW (при среднем риске) или FINANCE_REVIEW (при сумме от 50 000).
        if (risk == RiskLevel.MEDIUM) {
            return ApprovalRoute.DIRECTOR_REVIEW;
        }
        if (amount >= STANDARD_LIMIT) {
            return ApprovalRoute.FINANCE_REVIEW;
        }

        return ApprovalRoute.STANDARD;
    }

    // Вариант 4 (Часть Б): проверка соответствия заявки стандартному маршруту
    public boolean addStandardEligibility(long amount, boolean urgent, RiskLevel risk, boolean containsPersonalData) {
        if (amount < 0 || risk == null) {
            return false;
        }
        return amount < STANDARD_LIMIT && !urgent && risk == RiskLevel.LOW && !containsPersonalData;
    }

    // Консольный запуск для демонстрации
    public static void main(String[] args) {
        ApprovalRouter router = new ApprovalRouter();
        ApprovalRoute res = router.route(25_000L, false, RiskLevel.LOW, false);
        System.out.println("Маршрут заявки: " + res);
        System.out.println("Подходит под STANDARD (Часть Б): " + router.addStandardEligibility(25_000L, false, RiskLevel.LOW, false));
    }
}
