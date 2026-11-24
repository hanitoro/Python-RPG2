"""Комната 2. Лживый торговец.

Контракт функции total_cost(price, quantity, discount_percent=0):
- цена за штуку price >= 0;
- quantity — положительное целое число;
- скидка в процентах находится между 0 и 100;
- вернуть итоговую цену заказа, округлённую до 2 знаков;
- при нарушении условий вызвать ValueError.

Примеры:
total_cost(100, 2, 10) -> 180.0
total_cost(50, 1) -> 50.0

Исправь логику. Не переименовывай функцию.
"""


def total_cost(price, quantity, discount_percent=0):
    if price < 0:
        raise ValueError("Цена должна быть неотрицательной")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Количество должно быть положительным целым числом")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Скидка должна быть от 0 до 100 процентов")
    subtotal = price * quantity
    result = subtotal * (1 - discount_percent / 100)
    return round(result, 2)


if __name__ == "__main__":
    print("Покупка:", total_cost(100, 2, 10))
