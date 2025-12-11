import pytest
from src.abstracts import BaseProduct, BaseContainer
from src.models import Product, Smartphone, Category, Order
from src.mixins import ReprMixin


class TestAbstractClasses:

    def test_base_product_is_abstract(self):
        with pytest.raises(TypeError):
            BaseProduct("Test", "Test", 100.0, 5)

    def test_base_container_is_abstract(self):
        with pytest.raises(TypeError):
            BaseContainer("Test", "Test")

    def test_product_inherits_from_base_product(self):
        Product("Test", "Test", 100.0, 5)

    def test_category_inherits_from_base_container(self):
        category = Category("Test", "Test", [])
        assert isinstance(category, BaseContainer)

    def test_order_inherits_from_base_container(self):
        product = Product("Test", "Test", 100.0, 10)
        order = Order("Test", "Test", product, 2)
        assert isinstance(order, BaseContainer)


class TestReprMixin:

    def test_repr_mixin_logging(self, capsys):
        Product("Test", "Test", 100.0, 5)
        captured = capsys.readouterr()
        assert "Создан объект класса Product" in captured.out

    def test_repr_method(self):
        product = Product("Тестовый товар", "Описание", 100.0, 5)
        repr_str = repr(product)
        assert "Product" in repr_str
        assert ("Тестовый товар" in repr_str or
                "name='Тестовый товар'" in repr_str)
        assert "100.0" in repr_str or "price=100.0" in repr_str

    def test_repr_with_kwargs(self):
        smartphone = Smartphone(
            name="Test",
            description="Test",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        repr_str = repr(smartphone)
        assert "Smartphone" in repr_str
        assert "Test" in repr_str or "name='Test'" in repr_str
        assert "100.0" in repr_str or "price=100.0" in repr_str
        assert "model" in repr_str
        assert "128" in repr_str or "memory=128" in repr_str


class TestOrderClass:

    def test_order_creation(self):
        product = Product("Товар", "Описание", 100.0, 10)
        order = Order("Заказ1", "Первый заказ", product, 3)

        assert order.name == "Заказ1"
        assert order.product == product
        assert order.order_quantity == 3

    def test_order_total_cost(self):
        product = Product("Товар", "Описание", 150.0, 10)
        order = Order("Заказ1", "Описание", product, 4)

        assert order.total_cost == 600.0  # 150 * 4

    def test_order_total_quantity(self):
        product = Product("Товар", "Описание", 100.0, 10)
        order = Order("Заказ1", "Описание", product, 5)

        assert order.total_quantity == 5

    def test_order_insufficient_quantity(self):
        product = Product("Товар", "Описание", 100.0, 3)

        with pytest.raises(ValueError) as exc_info:
            Order("Заказ1", "Описание", product, 5)

        assert "Недостаточно товара" in str(exc_info.value)

    def test_process_order(self):
        product = Product("Товар", "Описание", 100.0, 10)
        order = Order("Заказ1", "Описание", product, 4)

        initial_quantity = product.quantity
        order.process_order()

        assert product.quantity == initial_quantity - order.order_quantity

    def test_order_count_increment(self):
        initial_count = Order.order_count \
            if hasattr(Order, 'order_count') else 0

        product = Product("Товар", "Описание", 100.0, 10)
        Order("Заказ1", "Описание", product, 2)

        product2 = Product("Товар2", "Описание2", 200.0, 5)
        Order("Заказ2", "Описание", product2, 1)

        assert Order.order_count == initial_count + 2


class TestInheritanceHierarchy:

    def test_mro_for_product(self):
        mro = Product.__mro__
        assert mro[0] == Product
        assert ReprMixin in mro
        assert BaseProduct in mro

    def test_multiple_inheritance(self):
        product = Product("Test", "Test", 100.0, 5)

        assert isinstance(product, Product)
        assert isinstance(product, ReprMixin)
        assert isinstance(product, BaseProduct)
        assert isinstance(product, object)

    def test_abstract_method_implementation(self):
        product = Product("Test", "Test", 100.0, 5)

        assert hasattr(product, '__str__')
        assert hasattr(product, '__add__')
        assert hasattr(product, 'price')
        assert hasattr(product.__class__, 'new_product')


class TestIntegration:

    def test_full_workflow(self):
        product1 = Product("Товар1", "Описание1", 100.0, 10)
        product2 = Smartphone(
            name="Смартфон",
            description="Android",
            price=200.0,
            quantity=5,
            efficiency=3.0,
            model="S23",
            memory=256,
            color="Blue"
        )

        category = Category("Техника", "Электроника", [product1, product2])

        order = Order("Мой заказ", "Заказ смартфона", product2, 2)

        assert category.total_quantity == 15
        assert order.total_cost == 400.0

        order.process_order()
        assert product2.quantity == 3

        assert str(product1) == "Товар1, 100 руб. Остаток: 10 шт."
        assert "Заказ: Мой заказ" in str(order)

    def test_category_and_order_common_interface(self):
        product = Product("Товар", "Описание", 100.0, 10)
        category = Category("Категория", "Описание", [product])
        order = Order("Заказ", "Описание", product, 3)

        assert hasattr(category, 'total_cost')
        assert hasattr(order, 'total_cost')
        assert hasattr(category, 'total_quantity')
        assert hasattr(order, 'total_quantity')

        assert isinstance(str(category), str)
        assert isinstance(str(order), str)
