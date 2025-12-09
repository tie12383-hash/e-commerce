class Product:
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list=None):
        if products_list is None:
            return cls(**product_data)

        for product in products_list:
            if product.name.lower() == product_data['name'].lower():
                product.description = product_data.get(
                    'description', product.description)

                new_price = product_data.get('price', product.price)
                if new_price > product.price:
                    product.price = new_price

                product.quantity += product_data.get('quantity', 0)

                return product

        return cls(**product_data)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: float):
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

    def __str__(self):
        if self.price.is_integer():
            price_str = str(int(self.price))
        else:
            price_str = str(self.price)

        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self):
        return "\n".join(str(product) for product in self.__products)

    @property
    def products_objects(self):
        return self.__products

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self.__products)


class CategoryIterator:

    def __init__(self, products: list):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration
