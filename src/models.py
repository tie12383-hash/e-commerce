class Product:
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        if products_list is None:
            products_list = []

        for existing_product in products_list:
            if existing_product.name.lower() == product_data['name'].lower():
                existing_product.quantity += product_data['quantity']

                if product_data['price'] > existing_product.price:
                    existing_product.price = product_data['price']

                return existing_product

        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price: float):
        if hasattr(self, '_price'):
            current_price = self._price
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

        self._price = new_price


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
        products_list = []
        for product in self.__products:
            price_str = str(product.price)
            if price_str.endswith('.0'):
                price_str = price_str[:-2]

            products_list.append(
                f"{product.name}, {price_str} руб. "
                f"Остаток: {product.quantity} шт."
            )
        return products_list

    @property
    def products_objects(self):
        return self.__products
