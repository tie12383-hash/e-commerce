import pytest
import os
from src.utils import load_data_from_json
from src.models import Category, Product


class TestUtils:
    def test_load_data_from_json(self):
        # Reset counters
        Category.category_count = 0
        Category.product_count = 0

        categories = load_data_from_json("products.json")

        assert isinstance(categories, list)
        assert len(categories) == 2
        assert all(isinstance(cat, Category) for cat in categories)

        # Check first category (Smartphones)
        smartphones = categories[0]
        assert smartphones.name == "Смартфоны"
        assert len(smartphones.products) == 3

        # Check products in smartphones category
        assert smartphones.products[0].name == "Samsung Galaxy C23 Ultra"
        assert smartphones.products[0].price == 180000.0
        assert smartphones.products[0].quantity == 5

        # Check second category (TVs)
        tvs = categories[1]
        assert tvs.name == "Телевизоры"
        assert len(tvs.products) == 1
        assert tvs.products[0].name == '55" QLED 4K'

        # Check counters
        assert Category.category_count == 2
        assert Category.product_count == 4

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_data_from_json("nonexistent.json")

    def test_loaded_products_attributes(self):
        Category.category_count = 0
        Category.product_count = 0

        categories = load_data_from_json("products.json")

        for category in categories:
            for product in category.products:
                assert hasattr(product, "name")
                assert hasattr(product, "description")
                assert hasattr(product, "price")
                assert hasattr(product, "quantity")
                assert isinstance(product.name, str)
                assert isinstance(product.description, str)
                assert isinstance(product.price, float)
                assert isinstance(product.quantity, int)
