from abc import ABC, abstractmethod


class Surface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError
