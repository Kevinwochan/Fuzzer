from abc import ABC, abstractmethod
from typing import List
from mutators.base_mutator import BaseMutator


class BaseHandler(ABC):
    @abstractmethod
    def __init__(self, filename: str, mutators: List[BaseMutator]):
        self.filename = filename
        self.data = self.__parse_to_list()
        self.raw_data = self.__parse_to_raw()

    @abstractmethod
    def __parse_to_list(self) -> list:
        pass

    @abstractmethod
    def __parse_to_raw(self) -> str:
        pass

    @abstractmethod
    def generate_input(self) -> str:
        pass
