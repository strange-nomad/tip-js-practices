package starter_project;

import java.util.Locale;
import java.util.Scanner;

/**
 * Расчётный модуль заказа для отдела закупок.
 * Выполнен в рамках Практической работы №3-4 (дисциплина «Информационные системы в бизнесе»).
 * Индивидуальный вариант № 4 (ставка НДС = 25%).
 */
public class OrderCalculator {

    // Индивидуальный вариант № 4: ставка НДС 25%
    public static final double VAT_RATE = 0.25;

    // Граничные константы предметной области
    public static final int MIN_QUANTITY = 1;
    public static final int MAX_QUANTITY = 10_000;

    public static final double MIN_PRICE = 0.01;
    public static final double MAX_PRICE = 5_000_000.0;

    public static final double MIN_DISCOUNT = 0.0;
    public static final double MAX_DISCOUNT = 30.0;

    /**
     * Вычисление базовой стоимости заказа (без учёта скидки и налога).
     *
     * @param quantity  количество единиц товара
     * @param unitPrice цена за единицу в рублях
     * @return базовая стоимость
     */
    public static double calculateBase(int quantity, double unitPrice) {
        return quantity * unitPrice;
    }

    /**
     * Вычисление суммы после применения процентной скидки.
     *
     * @param basePrice       базовая стоимость заказа
     * @param discountPercent скидка в процентах (0..30)
     * @return стоимость с учётом скидки
     */
    public static double applyDiscount(double basePrice, double discountPercent) {
        return basePrice * (1.0 - (discountPercent / 100.0));
    }

    /**
     * Вычисление абсолютной величины скидки в рублях.
     *
     * @param basePrice       базовая стоимость
     * @param discountPercent процент скидки
     * @return сумма скидки в рублях
     */
    public static double calculateDiscountAmount(double basePrice, double discountPercent) {
        return basePrice * (discountPercent / 100.0);
    }

    /**
     * Вычисление суммы НДС от стоимости со скидкой.
     * НДС рассчитывается строго после применения скидки.
     *
     * @param discountedPrice стоимость после вычета скидки
     * @param vatRate         ставка НДС (для Варианта 4 — 0.25)
     * @return начисленный НДС в рублях
     */
    public static double calculateVat(double discountedPrice, double vatRate) {
        return discountedPrice * vatRate;
    }

    /**
     * Проверка корректности входных параметров заказа.
     *
     * @param quantity        количество единиц (1..10000)
     * @param unitPrice       цена единицы (0.01..5000000.0)
     * @param discountPercent скидка в процентах (0..30)
     * @return true, если все параметры входят в допустимые диапазоны
     */
    public static boolean isValid(int quantity, double unitPrice, double discountPercent) {
        return (quantity >= MIN_QUANTITY && quantity <= MAX_QUANTITY)
                && (unitPrice >= MIN_PRICE && unitPrice <= MAX_PRICE)
                && (discountPercent >= MIN_DISCOUNT && discountPercent <= MAX_DISCOUNT);
    }

    /**
     * Получение текстового описания ошибки валидации входных данных.
     *
     * @param quantity        количество единиц
     * @param unitPrice       цена единицы
     * @param discountPercent скидка в процентах
     * @return описание первой обнаруженной ошибки или null при корректных данных
     */
    public static String getValidationError(int quantity, double unitPrice, double discountPercent) {
        if (quantity < MIN_QUANTITY || quantity > MAX_QUANTITY) {
            return String.format(Locale.US,
                    "Ошибка: Количество единиц (%d) выходит за допустимый диапазон [%d .. %d]",
                    quantity, MIN_QUANTITY, MAX_QUANTITY);
        }
        if (unitPrice < MIN_PRICE || unitPrice > MAX_PRICE) {
            return String.format(Locale.US,
                    "Ошибка: Цена единицы (%.2f руб.) выходит за допустимый диапазон [%.2f .. %.2f руб.]",
                    unitPrice, MIN_PRICE, MAX_PRICE);
        }
        if (discountPercent < MIN_DISCOUNT || discountPercent > MAX_DISCOUNT) {
            return String.format(Locale.US,
                    "Ошибка: Скидка (%.2f%%) выходит за допустимый диапазон [%.1f%% .. %.1f%%]",
                    discountPercent, MIN_DISCOUNT, MAX_DISCOUNT);
        }
        return null;
    }

    /**
     * Точка входа для интерактивного расчёта через консоль.
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        scanner.useLocale(Locale.US);

        System.out.println("==========================================================");
        System.out.println("  РАСЧЁТНЫЙ МОДУЛЬ ПАРАМЕТРОВ ЗАКАЗА (ВАРИАНТ № 4)");
        System.out.printf(Locale.US, "  Ставка НДС: %.0f%%\n", VAT_RATE * 100);
        System.out.println("==========================================================");

        try {
            System.out.print("Введите количество единиц (целое от 1 до 10 000): ");
            if (!scanner.hasNextInt()) {
                System.out.println("Ошибка ввода: Количество должно быть целым числом.");
                return;
            }
            int quantity = scanner.nextInt();

            System.out.print("Введите цену за единицу (руб., от 0.01 до 5 000 000.00): ");
            if (!scanner.hasNextDouble()) {
                System.out.println("Ошибка ввода: Цена должна быть числом.");
                return;
            }
            double unitPrice = scanner.nextDouble();

            System.out.print("Введите скидку (в %, от 0 до 30): ");
            if (!scanner.hasNextDouble()) {
                System.out.println("Ошибка ввода: Скидка должна быть числом.");
                return;
            }
            double discount = scanner.nextDouble();

            // Проверка диапазонов
            if (!isValid(quantity, unitPrice, discount)) {
                String error = getValidationError(quantity, unitPrice, discount);
                System.out.println("\n[ОТКАЗ В РАСЧЁТЕ] " + error);
                return;
            }

            // Выполнение расчёта через отдельные методы
            double baseAmount = calculateBase(quantity, unitPrice);
            double discountAmount = calculateDiscountAmount(baseAmount, discount);
            double discountedAmount = applyDiscount(baseAmount, discount);
            double vatAmount = calculateVat(discountedAmount, VAT_RATE);
            double totalAmount = discountedAmount + vatAmount;

            // Форматированный вывод в рублях с 2 знаками после запятой
            System.out.println("\n----------------- РЕЗУЛЬТАТ РАСЧЁТА -----------------");
            System.out.printf(Locale.US, "1. Базовая стоимость:       %12.2f руб.\n", baseAmount);
            System.out.printf(Locale.US, "2. Скидка (%.1f%%):           %12.2f руб.\n", discount, discountAmount);
            System.out.printf(Locale.US, "3. Стоимость со скидкой:    %12.2f руб.\n", discountedAmount);
            System.out.printf(Locale.US, "4. НДС (%.0f%%):              %12.2f руб.\n", VAT_RATE * 100, vatAmount);
            System.out.println("-----------------------------------------------------");
            System.out.printf(Locale.US, "ИТОГО К ОПЛАТЕ:             %12.2f руб.\n", totalAmount);
            System.out.println("-----------------------------------------------------");

        } catch (Exception e) {
            System.out.println("Непредвиденная ошибка при вводе данных: " + e.getMessage());
        } finally {
            scanner.close();
        }
    }
}
