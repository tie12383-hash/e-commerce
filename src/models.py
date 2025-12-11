from typing import Any, List
from .abstracts import BaseProduct, BaseContainer
from .mixins import ReprMixin


class Product(ReprMixin, BaseProduct):

    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(
            cls,
            product_data: dict,
            products_list: List['Product'] = None
    ) -> 'Product':
        base_product_data = {
            'name': product_data['name'],
            'description': product_data['description'],
            'price': product_data['price'],
            'quantity': product_data['quantity']
        }

        if products_list is None:
            return cls(**base_product_data)

        for product in products_list:
            if product.name.lower() == product_data['name'].lower():
                product.description = product_data.get(
                    'description', product.description
                )

                new_price = product_data.get('price', product.price)
                if new_price > product.price:
                    product.price = new_price

                product.quantity += product_data.get('quantity', 0)
                return product

        return cls(**base_product_data)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if hasattr(self, '_Product__price'):
            current_price = self.__price
        else:
            current_price = 0

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < current_price:
            response = input(
                f"Цена понижается с {current_price} до {new_price}. "
                "Подтвердите понижение цены (y/n): "
            )
            if response.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __str__(self) -> str:
        if self.price.is_integer():
            price_str = str(int(self.price))
        else:
            price_str = str(self.price)

        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        if not isinstance(other, Product):
            msg = "Можно складывать только объекты класса Product"
            raise TypeError(msg)

        if type(self) != type(other):
            msg = "Можно складывать только товары из одинаковых классов"
            raise TypeError(msg)

        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: float,
            model: str,
            memory: int,
            color: str
    ):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(
            cls,
            product_data: dict,
            products_list: List['Product'] = None
    ) -> 'Smartphone':
        smartphone_data = {
            'name': product_data['name'],
            'description': product_data['description'],
            'price': product_data['price'],
            'quantity': product_data['quantity'],
            'efficiency': product_data.get('efficiency', 0.0),
            'model': product_data.get('model', ''),
            'memory': product_data.get('memory', 0),
            'color': product_data.get('color', '')
        }

        if products_list is None:
            return cls(**smartphone_data)

        for product in products_list:
            if product.name.lower() == product_data['name'].lower():
                product.description = product_data.get(
                    'description', product.description
                )

                new_price = product_data.get('price', product.price)
                if new_price > product.price:
                    product.price = new_price

                product.quantity += product_data.get('quantity', 0)

                if isinstance(product, Smartphone):
                    product.efficiency = product_data.get(
                        'efficiency', product.efficiency
                    )
                    product.model = product_data.get('model', product.model)
                    product.memory = product_data.get('memory', product.memory)
                    product.color = product_data.get('color', product.color)

                return product

        return cls(**smartphone_data)

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str} (Модель: {self.model}, "
                f"Память: {self.memory}GB, Цвет: {self.color})")


class LawnGrass(Product):

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: int,
            color: str
    ):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(
            cls,
            product_data: dict,
            products_list: List['Product'] = None
    ) -> 'LawnGrass':
        grass_data = {
            'name': product_data['name'],
            'description': product_data['description'],
            'price': product_data['price'],
            'quantity': product_data['quantity'],
            'country': product_data.get('country', ''),
            'germination_period': product_data.get('germination_period', 0),
            'color': product_data.get('color', '')
        }

        if products_list is None:
            return cls(**grass_data)

        for product in products_list:
            if product.name.lower() == product_data['name'].lower():
                product.description = product_data.get(
                    'description', product.description
                )

                new_price = product_data.get('price', product.price)
                if new_price > product.price:
                    product.price = new_price

                product.quantity += product_data.get('quantity', 0)

                if isinstance(product, LawnGrass):
                    product.country = product_data.get(
                        'country', product.country
                    )
                    product.germination_period = product_data.get(
                        'germination_period', product.germination_period
                    )
                    product.color = product_data.get('color', product.color)

                return product

        return cls(**grass_data)

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str} (Страна: {self.country}, "
                f"Срок прорастания: {self.germination_period} дней, "
                f"Цвет: {self.color})")


class Category(BaseContainer):

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.__products = products
        super().__init__(name, description)

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            msg = "Можно добавлять только объекты класса Product"
            raise TypeError(msg)

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    @property
    def products_objects(self) -> List[Product]:
        return self.__products

    @property
    def total_cost(self) -> float:
        return sum(product.price * product.quantity
                   for product in self.__products)

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.__products)

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self.__products)


class Order(BaseContainer):

    order_count = 0

    def __init__(self, name: str, description: str,
                 product: Product, quantity: int):
        self.product = product
        self.order_quantity = quantity
        super().__init__(name, description)

        Order.order_count += 1

        if quantity > product.quantity:
            raise ValueError(f"Недостаточно товара '{product.name}'. "
                             f"Доступно: {product.quantity}, "
                             f"запрошено: {quantity}")

    @property
    def total_cost(self) -> float:
        return self.product.price * self.order_quantity

    @property
    def total_quantity(self) -> int:
        return self.order_quantity

    def __str__(self) -> str:
        return (f"Заказ: {self.name}\n"
                f"Товар: {self.product.name}\n"
                f"Количество: {self.order_quantity} шт.\n"
                f"Общая стоимость: {self.total_cost} руб.")

    def process_order(self) -> None:
        self.product.quantity -= self.order_quantity
        print(f"Заказ '{self.name}' обработан. "
              f"Остаток товара '{self.product.name}': "
              f"{self.product.quantity} шт.")


class CategoryIterator:

    def __init__(self, products: List[Product]):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Product:
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration
