import pytest
from src.models import Product, Category


@pytest.fixture
def sample_products():
    return [
        Product("Product1", "Description1", 100.0, 5),
        Product("Product2", "Description2", 200.0, 3)
    ]


class TestProduct:
    def test_product_initialization(self, sample_products):
        product = sample_products[0]
        assert product.name == "Product1"
        assert product.description == "Description1"
        assert product.price == 100.0
        assert product.quantity == 5


class TestCategory:
    def test_category_initialization(self, sample_products):
        Category.category_count = 0
        Category.product_count = 0

        category = Category("Category1", "Description1", sample_products)
        assert category.name == "Category1"
        assert category.description == "Description1"
        assert len(category.products) == 2
        assert Category.category_count == 1
        assert Category.product_count == 2

    def test_counters(self, sample_products):
        Category.category_count = 0
        Category.product_count = 0

        Category("Category1", "Description1", sample_products)
        Category("Category2", "Description2", [sample_products[0]])

        assert Category.category_count == 2
        assert Category.product_count == 3