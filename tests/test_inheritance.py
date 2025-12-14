import pytest
from src.models import Product, Smartphone, LawnGrass, Category
import io
import sys


class TestSmartphone:

    def test_smartphone_inheritance(self):
        smartphone = Smartphone(
            name="iPhone 15 Pro",
            description="Флагманский смартфон",
            price=120000.0,
            quantity=10,
            efficiency=3.5,
            model="iPhone 15 Pro",
            memory=256,
            color="Титан"
        )

        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, Smartphone)
        assert not isinstance(smartphone, LawnGrass)

    def test_smartphone_attributes(self):
        smartphone = Smartphone(
            name="Samsung Galaxy S23",
            description="Android смартфон",
            price=80000.0,
            quantity=15,
            efficiency=3.2,
            model="Galaxy S23",
            memory=128,
            color="Черный"
        )

        assert smartphone.name == "Samsung Galaxy S23"
        assert smartphone.price == 80000.0
        assert smartphone.quantity == 15
        assert smartphone.efficiency == 3.2
        assert smartphone.model == "Galaxy S23"
        assert smartphone.memory == 128
        assert smartphone.color == "Черный"

    def test_smartphone_str(self):
        smartphone = Smartphone(
            name="Xiaomi 13",
            description="Китайский смартфон",
            price=60000.0,
            quantity=20,
            efficiency=3.0,
            model="13",
            memory=256,
            color="Синий"
        )

        result = str(smartphone)
        assert "Xiaomi 13, 60000 руб. Остаток: 20 шт." in result
        assert "Модель: 13" in result
        assert "Память: 256GB" in result
        assert "Цвет: Синий" in result


class TestLawnGrass:

    def test_lawn_grass_inheritance(self):
        grass = LawnGrass(
            name="Газонная трава Премиум",
            description="Мягкая газонная трава",
            price=500.0,
            quantity=100,
            country="Россия",
            germination_period=14,
            color="Зеленый"
        )

        assert isinstance(grass, Product)
        assert isinstance(grass, LawnGrass)
        assert not isinstance(grass, Smartphone)

    def test_lawn_grass_attributes(self):
        grass = LawnGrass(
            name="Трава Спорт",
            description="Для спортивных площадок",
            price=700.0,
            quantity=50,
            country="Германия",
            germination_period=10,
            color="Темно-зеленый"
        )

        assert grass.name == "Трава Спорт"
        assert grass.price == 700.0
        assert grass.quantity == 50
        assert grass.country == "Германия"
        assert grass.germination_period == 10
        assert grass.color == "Темно-зеленый"

    def test_lawn_grass_str(self):
        grass = LawnGrass(
            name="Трава Декоративная",
            description="Для декоративных газонов",
            price=450.0,
            quantity=75,
            country="Италия",
            germination_period=21,
            color="Светло-зеленый"
        )

        result = str(grass)
        assert "Трава Декоративная, 450 руб. Остаток: 75 шт." in result
        assert "Страна: Италия" in result
        assert "Срок прорастания: 21 дней" in result
        assert "Цвет: Светло-зеленый" in result


class TestProductAddRestrictions:

    def test_add_same_class_products(self):
        smartphone1 = Smartphone(
            name="Phone1",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        smartphone2 = Smartphone(
            name="Phone2",
            description="Desc",
            price=200.0,
            quantity=3,
            efficiency=3.5,
            model="M2",
            memory=256,
            color="White"
        )

        result = smartphone1 + smartphone2
        expected = (100.0 * 5) + (200.0 * 3)
        assert result == expected

    def test_add_different_class_products_raises_error(self):
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        grass = LawnGrass(
            name="Grass",
            description="Desc",
            price=50.0,
            quantity=10,
            country="Russia",
            germination_period=14,
            color="Green"
        )

        with pytest.raises(TypeError) as exc_info:
            _ = smartphone + grass

        msg = "Можно складывать только товары из одинаковых классов"
        assert msg in str(exc_info.value)

    def test_add_base_product_with_smartphone_raises_error(self):
        base_product = Product("Base", "Desc", 100.0, 5)
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )

        with pytest.raises(TypeError) as exc_info:
            _ = base_product + smartphone

        msg = "Можно складывать только товары из одинаковых классов"
        assert msg in str(exc_info.value)

    def test_add_with_non_product_raises_error(self):
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )

        with pytest.raises(TypeError) as exc_info:
            _ = smartphone + 100

        msg = "Можно складывать только объекты класса Product"
        assert msg in str(exc_info.value)

        with pytest.raises(TypeError):
            _ = smartphone + "string"

        with pytest.raises(TypeError):
            _ = smartphone + [1, 2, 3]


class TestCategoryAddProductRestrictions:

    def test_add_product_valid(self):
        category = Category("Техника", "Описание", [])

        base_product = Product("Base", "Desc", 100.0, 5)
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        grass = LawnGrass(
            name="Grass",
            description="Desc",
            price=50.0,
            quantity=10,
            country="Russia",
            germination_period=14,
            color="Green"
        )

        category.add_product(base_product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category.products_objects) == 3

    def test_add_non_product_raises_error(self, capsys):
        category = Category("Техника", "Описание", [])

        category.add_product("не продукт")
        captured = capsys.readouterr()
        msg = "Можно добавлять только объекты класса Product"
        assert msg in captured.out
        assert len(category.products_objects) == 0

        category.add_product(123)
        captured = capsys.readouterr()
        assert msg in captured.out
        assert len(category.products_objects) == 0

        category.add_product({"name": "Test"})
        captured = capsys.readouterr()
        assert msg in captured.out
        assert len(category.products_objects) == 0

        category.add_product([1, 2, 3])
        captured = capsys.readouterr()
        assert msg in captured.out
        assert len(category.products_objects) == 0

        category.add_product(None)
        captured = capsys.readouterr()
        assert msg in captured.out
        assert len(category.products_objects) == 0

    def test_add_product_increases_counters(self):
        Category.category_count = 0
        Category.product_count = 0

        category = Category("Техника", "Описание", [])
        initial_count = Category.product_count

        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )

        category.add_product(smartphone)

        assert Category.product_count == initial_count + 1
        assert len(category.products_objects) == 1


class TestInheritanceHierarchy:

    def test_issubclass_relationships(self):
        assert issubclass(Smartphone, Product)
        assert issubclass(LawnGrass, Product)
        assert not issubclass(Smartphone, LawnGrass)
        assert not issubclass(LawnGrass, Smartphone)
        assert issubclass(Smartphone, object)
        assert issubclass(LawnGrass, object)
        assert issubclass(Product, object)

    def test_isinstance_relationships(self):
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        grass = LawnGrass(
            name="Grass",
            description="Desc",
            price=50.0,
            quantity=10,
            country="Russia",
            germination_period=14,
            color="Green"
        )

        assert isinstance(smartphone, Smartphone)
        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, object)
        assert not isinstance(smartphone, LawnGrass)

        assert isinstance(grass, LawnGrass)
        assert isinstance(grass, Product)
        assert isinstance(grass, object)
        assert not isinstance(grass, Smartphone)

    def test_type_comparison(self):
        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        grass = LawnGrass(
            name="Grass",
            description="Desc",
            price=50.0,
            quantity=10,
            country="Russia",
            germination_period=14,
            color="Green"
        )
        base_product = Product("Base", "Desc", 100.0, 5)

        assert type(smartphone) == Smartphone
        assert type(grass) == LawnGrass
        assert type(base_product) == Product
        assert type(smartphone) != type(grass)
        assert type(smartphone) != type(base_product)
        assert type(grass) != type(base_product)


class TestMixedCategoryOperations:

    def test_category_with_mixed_products(self):
        Category.category_count = 0
        Category.product_count = 0

        base_product = Product("Обычный товар", "Описание", 100.0, 10)
        smartphone = Smartphone(
            name="Смартфон",
            description="Флагманский",
            price=80000.0,
            quantity=5,
            efficiency=3.5,
            model="Pro",
            memory=256,
            color="Черный"
        )
        grass = LawnGrass(
            name="Трава",
            description="Декоративная",
            price=500.0,
            quantity=20,
            country="Россия",
            germination_period=14,
            color="Зеленый"
        )

        category = Category(
            "Разные товары",
            "Категория с разными типами",
            [base_product, smartphone, grass]
        )

        assert len(category.products_objects) == 3
        assert Category.category_count == 1
        assert Category.product_count == 3

        category_str = str(category)
        assert "Разные товары, количество продуктов: 35 шт." in category_str

        product_names = [p.name for p in category]
        assert product_names == ["Обычный товар", "Смартфон", "Трава"]

    def test_category_str_with_mixed_products(self):
        base_product = Product("Товар1", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Товар2",
            description="Смартфон",
            price=200.0,
            quantity=3,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )

        category = Category(
            "Категория",
            "Описание",
            [base_product, smartphone]
        )

        category_str = str(category)
        assert "Категория, количество продуктов: 8 шт." in category_str

    def test_category_products_getter_with_mixed(self):
        base_product = Product("Базовый", "Описание", 150.0, 2)
        smartphone = Smartphone(
            name="Смартфон",
            description="Android",
            price=300.0,
            quantity=4,
            efficiency=3.2,
            model="S23",
            memory=256,
            color="Blue"
        )

        category = Category(
            "Электроника",
            "Техника",
            [base_product, smartphone]
        )

        products_str = category.products
        assert "Базовый, 150 руб. Остаток: 2 шт." in products_str
        assert "Смартфон, 300 руб. Остаток: 4 шт." in products_str


class TestEdgeCases:

    def test_new_product_with_base_class_only(self):
        product_data = {
            'name': 'Новый продукт',
            'description': 'Описание нового продукта',
            'price': 100000.0,
            'quantity': 5
        }

        product = Product.new_product(product_data)

        assert isinstance(product, Product)
        assert product.name == 'Новый продукт'
        assert product.price == 100000.0
        assert product.quantity == 5

    def test_new_product_with_smartphone_class(self):
        smartphone_data = {
            'name': 'Новый смартфон',
            'description': 'Флагман',
            'price': 100000.0,
            'quantity': 5,
            'efficiency': 3.5,
            'model': 'Pro',
            'memory': 512,
            'color': 'Black'
        }

        smartphone = Smartphone.new_product(smartphone_data)

        assert isinstance(smartphone, Smartphone)
        assert smartphone.name == 'Новый смартфон'
        assert smartphone.price == 100000.0
        assert smartphone.quantity == 5
        assert smartphone.efficiency == 3.5
        assert smartphone.model == 'Pro'
        assert smartphone.memory == 512
        assert smartphone.color == 'Black'

    def test_new_product_with_lawn_grass_class(self):
        grass_data = {
            'name': 'Новая трава',
            'description': 'Декоративная',
            'price': 500.0,
            'quantity': 10,
            'country': 'Россия',
            'germination_period': 14,
            'color': 'Зеленый'
        }

        grass = LawnGrass.new_product(grass_data)

        assert isinstance(grass, LawnGrass)
        assert grass.name == 'Новая трава'
        assert grass.price == 500.0
        assert grass.quantity == 10
        assert grass.country == 'Россия'
        assert grass.germination_period == 14
        assert grass.color == 'Зеленый'

    def test_product_price_setter_in_inherited_classes(self):
        smartphone = Smartphone(
            name="Тест",
            description="Описание",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="Test",
            memory=128,
            color="Black"
        )

        smartphone.price = 150.0

        assert smartphone.price == 150.0

        captured_output = io.StringIO()
        sys.stdout = captured_output

        smartphone.price = -50.0

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "Цена не должна быть нулевая или отрицательная" in output
        assert smartphone.price == 150.0

    def test_empty_category_with_inherited_classes(self):
        category = Category("Пустая", "Описание", [])

        assert len(category.products_objects) == 0

        smartphone = Smartphone(
            name="Phone",
            description="Desc",
            price=100.0,
            quantity=5,
            efficiency=3.0,
            model="M1",
            memory=128,
            color="Black"
        )
        category.add_product(smartphone)

        assert len(category.products_objects) == 1
        assert isinstance(category.products_objects[0], Smartphone)

    def test_new_product_duplicate_update_for_smartphone(self):
        smartphone = Smartphone(
            name="iPhone",
            description="Старое описание",
            price=50000.0,
            quantity=10,
            efficiency=3.0,
            model="12",
            memory=128,
            color="Black"
        )

        category = Category("Техника", "Описание", [smartphone])

        update_data = {
            'name': 'iPhone',
            'description': 'Новое описание',
            'price': 60000.0,
            'quantity': 5,
            'efficiency': 3.5,
            'model': '13',
            'memory': 256,
            'color': 'Blue'
        }

        updated_smartphone = Smartphone.new_product(
            update_data,
            category.products_objects
        )

        assert updated_smartphone is smartphone
        assert smartphone.description == 'Новое описание'
        assert smartphone.price == 60000.0
        assert smartphone.quantity == 15
        assert smartphone.model == '13'
        assert smartphone.memory == 256
        assert smartphone.color == 'Blue'
