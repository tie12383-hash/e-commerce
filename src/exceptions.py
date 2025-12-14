class ZeroQuantityError(ValueError):

    def __init__(self, message="Товар с нулевым"
                               " количеством не может быть добавлен"):
        self.message = message
        super().__init__(self.message)


class EmptyCategoryError(ValueError):

    def __init__(self, message="Категория не содержит товаров"):
        self.message = message
        super().__init__(self.message)
