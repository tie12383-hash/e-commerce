import pytest
from src.models import Product, Category


@pytest.fixture
def sample_products():
    return [
        Product("Product1", "Description1", 100.0, 5),
        Product("Product2", "Description2", 200.0, 3)
    ]


@pytest.fixture
def sample_category(sample_products):
    Category.category_count = 0
    Category.product_count = 0
    return Category("Test Category", "Test Description", sample_products)


class TestProduct:
    def test_product_initialization(self, sample_products):
        product = sample_products[0]
        assert product.name == "Product1"
        assert product.description == "Description1"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_product_attributes_types(self, sample_products):
        product = sample_products[0]
        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_product_string_representation(self, sample_products):
        product = sample_products[0]
        assert hasattr(product, 'name')
        assert hasattr(product, 'description')
        assert hasattr(product, 'price')
        assert hasattr(product, 'quantity')


class TestCategory:
    def test_category_initialization(self, sample_category, sample_products):
        assert sample_category.name == "Test Category"
        assert sample_category.description == "Test Description"
        assert len(sample_category.products) == 2
        assert sample_category.products == sample_products

    def test_category_attributes_types(self, sample_category):
        assert isinstance(sample_category.name, str)
        assert isinstance(sample_category.description, str)
        assert isinstance(sample_category.products, list)

    def test_counters_increment(self):
        Category.category_count = 0
        Category.product_count = 0

        products1 = [Product("P1", "D1", 100.0, 1)]
        products2 = [
            Product("P2", "D2", 200.0, 2),
            Product("P3", "D3", 300.0, 3)
        ]

        category1 = Category("Cat1", "Desc1", products1)
        assert category1.name == "Cat1"
        assert Category.category_count == 1
        assert Category.product_count == 1

        category2 = Category("Cat2", "Desc2", products2)
        assert category2.name == "Cat2"
        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_empty_category(self):
        Category.category_count = 0
        Category.product_count = 0

        empty_category = Category("Empty", "No products", [])
        assert empty_category.name == "Empty"
        assert len(empty_category.products) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0

    def test_category_with_single_product(self):
        Category.category_count = 0
        Category.product_count = 0

        product = Product("Single", "One product", 50.0, 10)
        category = Category("Single", "One product category", [product])

        assert len(category.products) == 1
        assert category.products[0].name == "Single"
        assert Category.category_count == 1
        assert Category.product_count == 1
