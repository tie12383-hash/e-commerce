import pytest
from src.utils import load_data_from_json
from src.models import Category


class TestUtils:
    def test_load_data_from_json(self):
        Category.category_count = 0
        Category.product_count = 0

        categories = load_data_from_json('products.json')

        assert isinstance(categories, list)
        assert len(categories) == 2
        assert all(isinstance(cat, Category) for cat in categories)

        smartphones = categories[0]
        assert smartphones.name == "Смартфоны"
        assert len(smartphones.products_objects) == 3

        assert (smartphones.products_objects[0].name ==
                "Samsung Galaxy C23 Ultra")
        assert smartphones.products_objects[0].price == 180000.0
        assert smartphones.products_objects[0].quantity == 5

        tvs = categories[1]
        assert tvs.name == "Телевизоры"
        assert len(tvs.products_objects) == 1
        assert tvs.products_objects[0].name == "55\" QLED 4K"

        assert Category.category_count == 2
        assert Category.product_count == 4

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_data_from_json('nonexistent.json')

    def test_loaded_products_attributes(self):
        Category.category_count = 0
        Category.product_count = 0

        categories = load_data_from_json('products.json')

        for category in categories:
            for product in category.products_objects:
                assert hasattr(product, 'name')
                assert hasattr(product, 'description')
                assert hasattr(product, 'price')
                assert hasattr(product, 'quantity')
                assert isinstance(product.name, str)
                assert isinstance(product.description, str)
                assert isinstance(product.price, float)
                assert isinstance(product.quantity, int)
