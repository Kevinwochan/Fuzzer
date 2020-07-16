from typing import List
from abc import ABC, ABCMeta, abstractmethod


class BaseHandler(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, sample_filename: str):
        self._sample_filename = sample_filename
        self._data_raw = self.parse_to_raw()

    @abstractmethod
    def parse_to_raw(self) -> str:
        pass

    @abstractmethod
    def format_data_list(self, data: List[list]) -> str:
        pass

    @abstractmethod
    def generate_input(self) -> str:
        pass

    @property
    def sample_filename(self) -> str:
        return self._sample_filename

    @sample_filename.setter
    def set_sample_filename(self, sample_filename: str):
        self._sample_filename = sample_filename

    @property
    def data_list(self) -> List[list]:
        return self._data_list

    @data_list.setter
    def set_data_list(self, data_list: List[list]):
        self._data_list = data_list

    @property
    def data_raw(self) -> str:
        return self._data_raw

    @data_raw.setter
    def set_data_raw(self, data_raw: str):
        self._data_raw = data_raw
