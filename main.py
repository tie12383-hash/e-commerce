from src.models import Product, Category

if __name__ == "__main__":
    print("=== Тестирование новой функциональности ===\n")

    product1 = Product("Samsung Galaxy S23 Ultra",
                       "256GB, Серый цвет, 200MP камера",
                       180000.0, 5)
    product2 = Product("Iphone 15",
                       "512GB, Gray space",
                       210000.0, 8)

    category = Category("Смартфоны",
                        "Смартфоны как средство коммуникации",
                        [product1])

    print(f"Категория: {category.name}")
    print(f"Описание: {category.description}")
    print(f"Товаров в категории: {len(category.products_objects)}")

    category.add_product(product2)
    print(f"После добавления товаров: {len(category.products_objects)}")

    print("\nСписок товаров:")
    for product_str in category.products:
        print(f"  {product_str}")

    print("\n=== Тестирование класса-метода new_product ===")

    product_data = {
        'name': 'Xiaomi Redmi Note 11',
        'description': '1024GB, Синий',
        'price': 31000.0,
        'quantity': 14
    }

    products_list = category.products_objects
    product3 = Product.new_product(product_data, products_list)

    category.add_product(product3)

    print(f"\nПосле добавления через new_product: {len(category.products)}")
    for product_str in category.products:
        print(f"  {product_str}")

    print("\n=== Тестирование сеттера цены ===")

    print(f"Текущая цена продукта 1: {product1.price}")

    print("\nПопытка установить отрицательную цену:")
    product1.price = -100
    print(f"Цена после попытки: {product1.price}")

    print("\nПопытка установить нулевую цену:")
    product1.price = 0
    print(f"Цена после попытки: {product1.price}")

    print("\nУстановка корректной цены:")
    product1.price = 190000.0
    print(f"Цена после установки: {product1.price}")

    print("\n=== Счетчики ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\n=== Тестирование обработки дубликатов ===")

    duplicate_data = {
        'name': 'Samsung Galaxy S23 Ultra',
        'description': 'Новое описание',
        'price': 200000.0,
        'quantity': 3
    }

    product4 = Product.new_product(duplicate_data, category.products_objects)
    print("\nПосле обработки дубликата: ")
    print(f"  Количество товаров в категории: {len(category.products)}")
    print(f"  Цена обновленного товара: {product1.price} руб.")
    print(f"  Количество обновленного товара: {product1.quantity} шт.")
