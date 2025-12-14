from src.models import Product, Category, Order
from src.exceptions import ZeroQuantityError

if __name__ == "__main__":
    print("=== Тестирование обработки исключений ===\n")

    print("=== Создание продукта с нулевым количеством ===")
    try:
        product = Product("Товар с нулем", "Описание", 100.0, 0)
    except ZeroQuantityError as e:
        print(f"Поймано исключение: {e}")
    else:
        print("Продукт создан успешно")

    print("\n=== Создание продукта с нормальным количеством ===")
    try:
        product = Product("Нормальный товар", "Описание", 100.0, 5)
    except ZeroQuantityError as e:
        print(f"Поймано исключение: {e}")
    else:
        print("Продукт создан успешно")

    print("\n=== Создание и работа с категорией ===")
    category = Category("Техника", "Электроника", [])

    print("Добавление товаров в категорию:")
    product1 = Product("Товар1", "Описание1", 100.0, 3)
    category.add_product(product1)

    product2 = Product("Товар2", "Описание2", 200.0, 2)
    category.add_product(product2)

    print(f"\nСредняя цена в категории: {category.average_price()} руб.")
    print(f"Общее количество товаров: {category.total_quantity} шт.")

    print("\n=== Работа с пустой категорией ===")
    empty_category = Category("Пустая", "Описание", [])
    print(f"Средняя цена пустой категории: {empty_category.average_price()}")

    print("\n=== Создание заказа ===")
    try:
        order1 = Order("Заказ1", "Первый заказ", product1, 0)
    except Exception as e:
        print(f"Заказ не создан: {type(e).__name__} - {e}")

    try:
        order2 = Order("Заказ2", "Второй заказ", product1, 10)
    except Exception as e:
        print(f"Заказ не создан: {type(e).__name__} - {e}")

    try:
        order3 = Order("Заказ3", "Третий заказ", product1, 2)
        print(f"Заказ создан успешно: {order3}")
    except Exception as e:
        print(f"Заказ не создан: {type(e).__name__} - {e}")

    print("\n=== Обработка заказов ===")
    if 'order3' in locals():
        order3.process_order()
        print(f"Остаток товара: {product1.quantity} шт.")

    print("\n=== Счетчики ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
    print(f"Всего заказов: {Order.order_count}")
