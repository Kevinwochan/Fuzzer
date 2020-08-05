from abc import ABC, ABCMeta, abstractmethod

# This @decorator is totally optional, but it is a recommended best practice
try:  # We try to import GrahamDumpleton/wrapt if available
    from wrapt import decorator
except ImportError:  # fallback to the standard, less complete equivalent
    from functools import wraps as decorator

@decorator
def aslist(generator):
    "Function decorator to transform a generator into a list"
    def wrapper(*args, **kwargs):
        return list(generator(*args, **kwargs))
    return wrapper


class BaseHandler(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, data_raw: str):
        self._data_raw = data_raw
    
    @abstractmethod
    def generate_input(self):
        pass

    @property
    def data_raw(self) -> str:
        return self._data_raw
