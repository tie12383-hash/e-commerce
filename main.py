from src.models import Product, Smartphone, LawnGrass, Category

if __name__ == "__main__":
    print("=== Тестирование новой функциональности "
          "с классами-наследниками ===\n")

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

    print(f"1. Базовый продукт: {base_product}")
    print(f"2. Смартфон: {smartphone}")
    print(f"3. Газонная трава: {lawn_grass}")

    print("\n=== Тестирование сложения продуктов ===")

    print("1. Сложение двух смартфонов:")
    smartphone2 = Smartphone(
        "Samsung Galaxy S23",
        "Android смартфон",
        80000.0,
        3,
        efficiency=3.2,
        model="Galaxy S23",
        memory=128,
        color="Черный"
    )

    try:
        total_smartphones = smartphone + smartphone2
        print(f"   Общая стоимость смартфонов: {total_smartphones} руб.")
        print(f"   Расчет: ({smartphone.price} × {smartphone.quantity}) + "
              f"({smartphone2.price} × {smartphone2.quantity})")
    except TypeError as e:
        print(f"   Ошибка: {e}")

    print("\n2. Сложение базовых продуктов (должно работать):")
    base_product2 = Product("Другой товар", "Описание", 300.0, 8)
    try:
        total_base = base_product + base_product2
        print(f"   Общая стоимость базовых товаров: {total_base} руб.")
    except TypeError as e:
        print(f"   Ошибка: {e}")

    print("\n3. Сложение разных классов (должно вызвать ошибку):")
    try:
        invalid_total = smartphone + lawn_grass
        print(f"   Результат: {invalid_total} руб.")
    except TypeError as e:
        print(f"   Ожидаемая ошибка: {e}")

    print("\n4. Сложение продукта с числом (должно вызвать ошибку):")
    try:
        invalid_total = smartphone + 100
        print(f"   Результат: {invalid_total} руб.")
    except TypeError as e:
        print(f"   Ожидаемая ошибка: {e}")

    print("\n=== Тестирование категорий ===")

    category = Category(
        "Разные товары",
        "Категория содержит товары разных типов",
        [base_product, smartphone, lawn_grass]
    )

    print(f"Категория: {category}")
    print(f"Количество товаров в категории: {len(category.products_objects)}")

    print("\n=== Добавление нового продукта в категорию ===")

    new_smartphone = Smartphone(
        "Xiaomi 13",
        "Китайский смартфон",
        60000.0,
        8,
        efficiency=3.0,
        model="13",
        memory=256,
        color="Синий"
    )

    category.add_product(new_smartphone)
    print(f"После добавления смартфона: "
          f"{len(category.products_objects)} товаров")

    print("\n=== Попытка добавить не-продукт в категорию ===")
    try:
        category.add_product("не продукт")
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    print("\n=== Итерация по товарам в категории ===")
    print("Список товаров:")
    for i, product in enumerate(category, 1):
        print(f"  {i}. {product}")

    print("\n=== Тестирование isinstance и issubclass ===")

    print("1. Проверка isinstance:")
    print(f"   smartphone является Smartphone: "
          f"{isinstance(smartphone, Smartphone)}")
    print(f"   smartphone является Product: "
          f"{isinstance(smartphone, Product)}")
    print(f"   smartphone является LawnGrass: "
          f"{isinstance(smartphone, LawnGrass)}")

    print("\n2. Проверка issubclass:")
    print(f"   Smartphone является подклассом Product: "
          f"{issubclass(Smartphone, Product)}")
    print(f"   LawnGrass является подклассом Product: "
          f"{issubclass(LawnGrass, Product)}")
    print(f"   Smartphone является подклассом LawnGrass: "
          f"{issubclass(Smartphone, LawnGrass)}")

    print("\n=== Тестирование сеттера цены ===")
    print(f"Текущая цена смартфона: {smartphone.price} руб.")

    print("Попытка установить отрицательную цену:")
    smartphone.price = -100
    print(f"Цена после попытки: {smartphone.price} руб.")

    print("Установка корректной цены:")
    smartphone.price = 125000.0
    print(f"Цена после установки: {smartphone.price} руб.")

    print("\n=== Счетчики ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\n=== Тестирование метода new_product ===")

    product_data = {
        'name': 'Новый продукт',
        'description': 'Описание нового продукта',
        'price': 3000.0,
        'quantity': 7
    }

    new_product = Product.new_product(product_data, category.products_objects)
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
