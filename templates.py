from abc import ABC, abstractmethod

import pygame as pg

from helpers import Point


class Surface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> pg.Surface:
        raise NotImplementedError

    @abstractmethod
    def process_inputs(self, mouse_position: Point):
        raise NotImplementedError