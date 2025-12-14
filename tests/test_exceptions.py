import pytest
from src.models import Product, Smartphone, Category, Order
from src.exceptions import ZeroQuantityError


class TestZeroQuantityProduct:

    def test_product_creation_with_zero_quantity(self):
        with pytest.raises(ZeroQuantityError) as exc_info:
            Product("Тестовый товар", "Описание", 100.0, 0)

        assert "Товар с нулевым количеством не может быть добавлен" in str(
            exc_info.value)

    def test_smartphone_creation_with_zero_quantity(self):
        with pytest.raises(ZeroQuantityError) as exc_info:
            Smartphone(
                name="Телефон",
                description="Описание",
                price=100.0,
                quantity=0,
                efficiency=3.0,
                model="Test",
                memory=128,
                color="Black"
            )

        assert "Товар с нулевым количеством не может быть добавлен" in str(
            exc_info.value)

    def test_product_creation_with_positive_quantity(self):
        product = Product("Тестовый товар", "Описание", 100.0, 5)
        assert product.quantity == 5
        assert isinstance(product, Product)


class TestCategoryAveragePrice:

    def test_average_price_with_products(self):
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3),
            Product("Товар3", "Описание3", 300.0, 2)
        ]

        category = Category("Категория", "Описание", products)
        average = category.average_price()

        expected_average = (100.0 + 200.0 + 300.0) / 3
        assert average == expected_average

    def test_average_price_empty_category(self, capsys):
        category = Category("Пустая категория", "Описание", [])

        average = category.average_price()

        captured = capsys.readouterr()
        assert "Категория не содержит товаров" in captured.out
        assert average == 0

    def test_average_price_single_product(self):
        product = Product("Товар", "Описание", 150.0, 3)
        category = Category("Категория", "Описание", [product])

        average = category.average_price()
        assert average == 150.0


class TestCategoryAddProductExceptions:

    def test_add_product_successful(self, capsys):
        category = Category("Категория", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)

        category.add_product(product)

        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category.products_objects) == 1


class TestOrderExceptions:

    def test_order_with_zero_quantity(self, capsys):
        product = Product("Товар", "Описание", 100.0, 10)

        with pytest.raises(ZeroQuantityError) as exc_info:
            Order("Заказ", "Описание", product, 0)

        captured = capsys.readouterr()
        assert "Количество товара в заказе не может быть нулевым" in str(
            exc_info.value)
        assert "Обработка создания заказа завершена" in captured.out

    def test_order_with_insufficient_quantity(self, capsys):
        product = Product("Товар", "Описание", 100.0, 3)

        with pytest.raises(ValueError) as exc_info:
            Order("Заказ", "Описание", product, 5)

        captured = capsys.readouterr()
        assert "Недостаточно товара" in str(exc_info.value)
        assert "Обработка создания заказа завершена" in captured.out

    def test_order_successful_creation(self, capsys):
        product = Product("Товар", "Описание", 100.0, 10)

        order = Order("Заказ", "Описание", product, 3)

        captured = capsys.readouterr()
        assert "Заказ успешно создан" in captured.out
        assert "Обработка создания заказа завершена" in captured.out
        assert order.order_quantity == 3

    def test_process_order_with_insufficient_quantity(self, capsys):
        product = Product("Товар", "Описание", 100.0, 2)
        order = Order("Заказ", "Описание", product, 2)

        product.quantity = 1

        order.process_order()

        captured = capsys.readouterr()
        assert "Недостаточно товара" in captured.out
        assert "Обработка заказа завершена" in captured.out

    def test_process_order_successful(self, capsys):
        product = Product("Товар", "Описание", 100.0, 10)
        order = Order("Заказ", "Описание", product, 3)

        order.process_order()

        captured = capsys.readouterr()
        assert "Заказ 'Заказ' успешно обработан" in captured.out
        assert "Обработка заказа завершена" in captured.out
        assert product.quantity == 7


class TestNewProductExceptions:

    def test_new_product_with_zero_quantity(self):
        product_data = {
            'name': 'Новый товар',
            'description': 'Описание',
            'price': 100.0,
            'quantity': 0
        }

        with pytest.raises(ZeroQuantityError):
            Product.new_product(product_data)


class TestIntegrationExceptions:

    def test_full_workflow_with_exceptions(self, capsys):
        category = Category("Техника", "Электроника", [])

        product1 = Product("Товар1", "Описание1", 100.0, 5)
        category.add_product(product1)

        product2 = Product("Товар2", "Описание2", 200.0, 3)
        category.add_product(product2)

        average = category.average_price()
        assert average == 150.0

        order = Order("Мой заказ", "Описание", product1, 2)

        order.process_order()

        captured = capsys.readouterr()
        assert "Товар успешно добавлен" in captured.out
        assert "Заказ успешно создан" in captured.out
        assert "успешно обработан" in captured.out
        assert "Обработка" in captured.out

        assert product1.quantity == 3  # 5 - 2
        assert order.total_cost == 200.0  # 100 * 2

    def test_edge_cases(self):
        empty_category = Category("Пустая", "Описание", [])
        assert empty_category.total_quantity == 0
        assert empty_category.total_cost == 0.0
        assert empty_category.average_price() == 0.0
