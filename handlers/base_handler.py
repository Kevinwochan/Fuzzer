from abc import ABC, ABCMeta, abstractmethod


class BaseHandler(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, data_raw: str):
        self._data_raw = data_raw

    @abstractmethod
    def generate_input(self) -> str:
        pass

    @property
    def data_raw(self) -> str:
        return self._data_raw
