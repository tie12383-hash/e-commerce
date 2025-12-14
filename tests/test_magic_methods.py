import pytest
from src.models import Product, Category, CategoryIterator


class TestProductStrMethod:

    def test_product_str_with_integer_price(self):
        product = Product("Телефон", "Описание", 100.0, 5)
        expected = "Телефон, 100 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_str_with_float_price(self):
        product = Product("Телефон", "Описание", 99.99, 5)
        expected = "Телефон, 99.99 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_str_with_large_price(self):
        product = Product("Ноутбук", "Игровой", 150000.0, 2)
        expected = "Ноутбук, 150000 руб. Остаток: 2 шт."
        assert str(product) == expected


class TestCategoryStrMethod:

    def test_category_str_empty(self):
        category = Category("Пустая", "Описание", [])
        expected = "Пустая, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_str_single_product(self):
        product = Product("Телефон", "Описание", 100.0, 5)
        category = Category("Техника", "Описание", [product])
        expected = "Техника, количество продуктов: 5 шт."
        assert str(category) == expected

    def test_category_str_multiple_products(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
            Product("Товар3", "Описание3", 300.0, 1)
        ]
        category = Category("Техника", "Описание", products)
        expected = "Техника, количество продуктов: 6 шт."
        assert str(category) == expected


class TestProductAddMethod:

    def test_product_add_valid(self):
        product1 = Product("Товар1", "Описание1", 100.0, 10)
        product2 = Product("Товар2", "Описание2", 200.0, 5)

        result = product1 + product2
        expected = (100.0 * 10) + (200.0 * 5)

        assert result == expected
        assert isinstance(result, float)

    def test_product_add_with_different_types(self):
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(TypeError):
            _ = product + 100

        with pytest.raises(TypeError):
            _ = product + "строка"

        with pytest.raises(TypeError):
            _ = product + [1, 2, 3]

    def test_product_add_commutative(self):
        product1 = Product("Товар1", "Описание1", 100.0, 3)
        product2 = Product("Товар2", "Описание2", 200.0, 4)

        result1 = product1 + product2
        result2 = product2 + product1

        assert result1 == result2

    def test_product_add_zero_price(self):
        product1 = Product("Товар1", "Описание1", 0.0, 10)
        product2 = Product("Товар2", "Описание2", 200.0, 5)

        result = product1 + product2
        expected = (0.0 * 10) + (200.0 * 5)

        assert result == expected


class TestCategoryIterator:

    def test_category_iterator_creation(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        category = Category("Техника", "Описание", products)

        iterator = iter(category)
        assert isinstance(iterator, CategoryIterator)

    def test_category_iterator_iteration(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3),
            Product("Товар3", "Описание3", 300.0, 2)
        ]
        category = Category("Техника", "Описание", products)

        collected_products = []
        for product in category:
            collected_products.append(product)

        assert len(collected_products) == 3
        assert collected_products[0].name == "Товар1"
        assert collected_products[1].name == "Товар2"
        assert collected_products[2].name == "Товар3"

    def test_category_iterator_empty(self):
        category = Category("Пустая", "Описание", [])

        collected_products = []
        for product in category:
            collected_products.append(product)

        assert len(collected_products) == 0

    def test_category_iterator_direct_usage(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        iterator = CategoryIterator(products)

        assert next(iterator).name == "Товар1"
        assert next(iterator).name == "Товар2"

        with pytest.raises(StopIteration):
            next(iterator)

    def test_category_iterator_reset(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        category = Category("Техника", "Описание", products)

        count1 = 0
        for _ in category:
            count1 += 1

        count2 = 0
        for _ in category:
            count2 += 1

        assert count1 == count2 == 2


class TestIntegrationFeatures:

    def test_products_getter_uses_str(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        category = Category("Техника", "Описание", products)

        products_str = category.products
        assert "Товар1, 100 руб. Остаток: 5 шт." in products_str
        assert "Товар2, 200 руб. Остаток: 3 шт." in products_str

    def test_full_workflow_with_magic_methods(self):
        Category.category_count = 0
        Category.product_count = 0

        phone = Product("Смартфон", "Android", 50000.0, 10)
        tablet = Product("Планшет", "10 дюймов", 30000.0, 5)

        total_value = phone + tablet
        expected_value = (50000.0 * 10) + (30000.0 * 5)
        assert total_value == expected_value

        electronics = Category("Электроника", "Техника", [phone, tablet])

        category_str = str(electronics)
        assert "Электроника, количество продуктов: 15 шт." == category_str

        assert str(phone) == "Смартфон, 50000 руб. Остаток: 10 шт."

        product_names = [p.name for p in electronics]
        assert product_names == ["Смартфон", "Планшет"]

        products_list_str = electronics.products
        assert "Смартфон, 50000 руб. Остаток: 10 шт." in products_list_str
        assert "Планшет, 30000 руб. Остаток: 5 шт." in products_list_str

    def test_new_product_method_updates(self):
        initial_product = Product("Телефон", "Старое описание", 10000.0, 5)

        update_data = {
            'name': 'Телефон',
            'description': 'Новое описание',
            'price': 12000.0,
            'quantity': 3
        }

        updated_product = Product.new_product(update_data, [initial_product])

        assert updated_product is initial_product
        assert updated_product.description == 'Новое описание'
        assert updated_product.price == 12000.0
        assert updated_product.quantity == 8  # 5 + 3


class TestEdgeCases:

    def test_product_add_same_product(self):
        product = Product("Товар", "Описание", 100.0, 5)
        result = product + product
        expected = (100.0 * 5) * 2
        assert result == expected

    def test_category_str_with_none_products(self):
        category = Category("Категория", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 1)
        category._Category__products.append(product)
        product.quantity = 0

        assert str(category) == "Категория, количество продуктов: 0 шт."

    def test_category_iter_with_modified_products(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        category = Category("Техника", "Описание", products.copy())

        for i, product in enumerate(category):
            if i == 0:
                product.quantity = 10

        assert category.products_objects[0].quantity == 10
