import json
from .models import Category, Product


def load_data_from_json(file_path: str) -> list[Category]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = [
            Product(
                name=product['name'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity']
            )
            for product in category_data['products']
        ]
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories