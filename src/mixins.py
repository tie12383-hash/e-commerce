class ReprMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"Создан объект класса {self.__class__.__name__}")

    def __repr__(self) -> str:
        attrs = []

        if hasattr(self, 'name'):
            attrs.append(f"name='{self.name}'")
        if hasattr(self, 'description'):
            attrs.append(f"description='{self.description}'")
        if hasattr(self, 'price'):
            attrs.append(f'price={self.price}')
        if hasattr(self, 'quantity'):
            attrs.append(f'quantity={self.quantity}')

        if hasattr(self, 'efficiency'):
            attrs.append(f'efficiency={self.efficiency}')
        if hasattr(self, 'model'):
            attrs.append(f"model='{self.model}'")
        if hasattr(self, 'memory'):
            attrs.append(f'memory={self.memory}')
        if hasattr(self, 'color'):
            attrs.append(f"color='{self.color}'")

        if hasattr(self, 'country'):
            attrs.append(f"country='{self.country}'")
        if hasattr(self, 'germination_period'):
            attrs.append(f'germination_period={self.germination_period}')

        return f"{self.__class__.__name__}({', '.join(attrs)})"
