package ru.edu.pr01;

import java.util.Locale;
import java.util.Scanner;

public class OrderCalculator {

    // Вариант 4: ставка НДС 25%
    public static final double VAT_RATE = 25.0;

    public static boolean isValid(int quantity, double unitPrice, double discountPercent) {
        return quantity > 0 && quantity <= 10_000
                && unitPrice > 0 && unitPrice <= 5_000_000.0
                && discountPercent >= 0 && discountPercent <= 30.0;
    }

    public static double calculateBase(int quantity, double unitPrice) {
        return quantity * unitPrice;
    }

    public static double applyDiscount(double base, double discountPercent) {
        return base * (1.0 - discountPercent / 100.0);
    }

    public static double calculateVat(double discounted, double vatPercent) {
        return discounted * (vatPercent / 100.0);
    }

    public static double calculateTotal(int quantity, double unitPrice, double discountPercent, double vatPercent) {
        double base = calculateBase(quantity, unitPrice);
        double discounted = applyDiscount(base, discountPercent);
        double vat = calculateVat(discounted, vatPercent);
        return discounted + vat;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        scanner.useLocale(Locale.US);

        System.out.print("Введите количество, цену и скидку (%): ");
        if (!scanner.hasNextInt()) {
            System.out.println("Ошибка: неверное количество");
            return;
        }
        int quantity = scanner.nextInt();

        if (!scanner.hasNextDouble()) {
            System.out.println("Ошибка: неверная цена");
            return;
        }
        double unitPrice = scanner.nextDouble();

        if (!scanner.hasNextDouble()) {
            System.out.println("Ошибка: неверная скидка");
            return;
        }
        double discountPercent = scanner.nextDouble();

        if (!isValid(quantity, unitPrice, discountPercent)) {
            System.out.println("Ошибка: параметры выходят за допустимые границы");
            return;
        }

        double total = calculateTotal(quantity, unitPrice, discountPercent, VAT_RATE);
        System.out.printf(Locale.US, "Итого к оплате: %.2f руб.\n", total);
    }
}
