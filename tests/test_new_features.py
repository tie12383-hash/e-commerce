import pytest
from src.models import Product, Category


class TestPrivateAttributes:

    def test_category_products_is_private(self):
        product = Product("Test", "Test", 100.0, 5)
        category = Category("Test", "Test", [product])

        assert hasattr(category, '_Category__products')

        with pytest.raises(AttributeError):
            _ = category.__products


class TestAddProductMethod:

    def test_add_product_increases_count(self):
        Category.category_count = 0
        Category.product_count = 0

        product1 = Product("P1", "D1", 100.0, 1)
        product2 = Product("P2", "D2", 200.0, 2)
        category = Category("Test", "Test", [product1])

        assert Category.product_count == 1

        category.add_product(product2)
        assert Category.product_count == 2

    def test_add_product_only_accepts_product(self):
        category = Category("Test", "Test", [])

        with pytest.raises(TypeError):
            category.add_product("not a product")

        with pytest.raises(TypeError):
            category.add_product({"name": "Test"})


class TestProductsGetter:

    def test_products_getter_returns_string(self):
        product = Product("Товар", "Описание", 80.0, 15)
        category = Category("Категория", "Описание", [product])

        result = category.products
        assert isinstance(result, str)
        assert "Товар, 80 руб. Остаток: 15 шт." in result

    def test_products_getter_with_multiple_products(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 10)
        ]
        category = Category("Категория", "Описание", products)

        result = category.products
        assert isinstance(result, str)
        assert "Товар1, 100 руб. Остаток: 5 шт." in result
        assert "Товар2, 200 руб. Остаток: 10 шт." in result
        assert result.count('\n') == 1


class TestNewProductClassMethod:

    def test_new_product_creates_instance(self):
        product_data = {
            'name': 'Новый товар',
            'description': 'Описание',
            'price': 100.0,
            'quantity': 5
        }

        product = Product.new_product(product_data)

        assert isinstance(product, Product)
        assert product.name == 'Новый товар'
        assert product.price == 100.0
        assert product.quantity == 5

    def test_new_product_accepts_only_dict(self):
        product_data = {
            'name': 'Товар',
            'description': 'Описание',
            'price': 100.0,
            'quantity': 5
        }

        product = Product.new_product(product_data)
        assert isinstance(product, Product)

        with pytest.raises(TypeError):
            Product.new_product("not a dict")

        with pytest.raises(TypeError):
            Product.new_product(['name', 'Товар'])


class TestPriceGetterSetter:

    def test_price_getter(self):
        product = Product("Товар", "Описание", 100.0, 5)
        assert product.price == 100.0

    def test_price_setter_positive_value(self):
        product = Product("Товар", "Описание", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_zero_value(self, capsys):
        product = Product("Товар", "Описание", 100.0, 5)
        product.price = 0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_price_setter_negative_value(self, capsys):
        product = Product("Товар", "Описание", 100.0, 5)
        product.price = -50.0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_price_lowering_with_confirmation(self, monkeypatch):
        product = Product("Товар", "Описание", 100.0, 5)

        monkeypatch.setattr('builtins.input', lambda _: 'y')
        product.price = 80.0

        assert product.price == 80.0

    def test_price_lowering_without_confirmation(self, monkeypatch, capsys):
        product = Product("Товар", "Описание", 100.0, 5)

        monkeypatch.setattr('builtins.input', lambda _: 'n')
        product.price = 80.0

        captured = capsys.readouterr()
        assert "Изменение цены отменено" in captured.out
        assert product.price == 100.0

    def test_price_increasing_no_confirmation_needed(self):
        product = Product("Товар", "Описание", 100.0, 5)
        product.price = 150.0

        assert product.price == 150.0

    def test_price_is_truly_private(self):
        product = Product("Товар", "Описание", 100.0, 5)

        assert hasattr(product, '_Product__price')

        with pytest.raises(AttributeError):
            _ = product.__price

        assert product.price == 100.0


class TestIntegration:

    def test_full_workflow(self):
        Category.category_count = 0
        Category.product_count = 0

        product1 = Product("Товар1", "Описание1", 100.0, 10)
        product2 = Product("Товар2", "Описание2", 200.0, 5)

        category = Category("Категория", "Описание", [product1])
        assert len(category.products_objects) == 1
        assert Category.category_count == 1
        assert Category.product_count == 1

        category.add_product(product2)
        assert len(category.products_objects) == 2
        assert Category.product_count == 2

        products_str = category.products
        assert isinstance(products_str, str)
        assert "Товар1, 100 руб. Остаток: 10 шт." in products_str
        assert "Товар2, 200 руб. Остаток: 5 шт." in products_str
