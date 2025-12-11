from src.models import Product, Smartphone, LawnGrass, Category, Order

if __name__ == "__main__":
    print("=== Тестирование новой функциональности "
          "с классами-наследниками и абстрактными классами ===\n")

    print("=== Создание объектов разных классов ===")

    base_product = Product(
        "Обычный товар",
        "Просто товар без специфических характеристик",
        500.0,
        10
    )

    smartphone = Smartphone(
        "iPhone 15 Pro",
        "Флагманский смартфон Apple",
        120000.0,
        5,
        efficiency=3.5,
        model="iPhone 15 Pro",
        memory=256,
        color="Титан"
    )

    lawn_grass = LawnGrass(
        "Газонная трава Премиум",
        "Мягкая трава для газонов",
        800.0,
        20,
        country="Россия",
        germination_period=14,
        color="Зеленый"
    )

    print(f"\n1. Базовый продукт: {base_product}")
    print(f"2. Смартфон: {smartphone}")
    print(f"3. Газонная трава: {lawn_grass}")

    print("\n=== Тестирование __repr__ ===")
    print(f"Repr базового продукта: {repr(base_product)}")
    print(f"Repr смартфона: {repr(smartphone)}")
    print(f"Repr газонной травы: {repr(lawn_grass)}")

    print("\n=== Создание категории ===")
    category = Category(
        "Разные товары",
        "Категория содержит товары разных типов",
        [base_product, smartphone, lawn_grass]
    )

    print(f"Категория: {category}")
    print(f"Общая стоимость категории: {category.total_cost} руб.")

    print("\n=== Создание заказа ===")
    try:
        order = Order(
            name="Мой первый заказ",
            description="Заказ iPhone 15 Pro",
            product=smartphone,
            quantity=2
        )

        print("Заказ создан успешно:")
        print(order)

        print("\n=== Обработка заказа ===")
        order.process_order()

    except ValueError as e:
        print(f"Ошибка создания заказа: {e}")

    print("\n=== Проверка абстрактных классов ===")
    print(f"Product является экземпляром BaseProduct: "
          f"{isinstance(base_product, Product)}")
    print(f"Category является экземпляром BaseContainer: "
          f"{isinstance(category, Category)}")
    print(f"Order является экземпляром BaseContainer: "
          f"{isinstance(order, Order)}")

    print("\n=== Счетчики ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
    print(f"Всего заказов: {Order.order_count}")

    print("\n=== Тестирование метода new_product ===")

    product_data = {
        'name': 'Новый продукт',
        'description': 'Описание нового продукта',
        'price': 3000.0,
        'quantity': 7
    }

    new_product = Product.new_product(product_data,
                                      category.products_objects)
    print(f"Создан новый продукт: {new_product}")

    print("\n=== Проверка обработки дубликатов для смартфона ===")

    duplicate_smartphone_data = {
        'name': 'iPhone 15 Pro',
        'description': 'Обновленное описание',
        'price': 130000.0,
        'quantity': 3,
        'efficiency': 3.8,
        'model': 'iPhone 15 Pro Max',
        'memory': 512,
        'color': 'Темный титан'
    }

    updated_smartphone = Smartphone.new_product(
        duplicate_smartphone_data,
        category.products_objects
    )
    print("После обработки дубликата смартфона:")
    print(f"  Найденный продукт: {smartphone.name}")
    print(f"  Новая цена: {smartphone.price} руб.")
    print(f"  Новое количество: {smartphone.quantity} шт.")
    print(f"  Новая модель: {smartphone.model}")
    print(f"  Новая память: {smartphone.memory}GB")
    print(f"  Новый цвет: {smartphone.color}")
