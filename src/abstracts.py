from abc import ABC, abstractmethod
from typing import Any, List


class BaseProduct(ABC):

    @abstractmethod
    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> float:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: dict,
                    products_list: List['BaseProduct'] = None) -> \
            'BaseProduct':
        pass


class BaseContainer(ABC):

    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abstractmethod
    def total_cost(self) -> float:
        pass

    @property
    @abstractmethod
    def total_quantity(self) -> int:
        pass
