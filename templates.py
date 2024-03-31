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

    def update(self, mouse_position: Point | None) -> None:  # noqa: B027
        """Update game for 1 frame. Mouse position is relative to surface.

        Mouse position is None if the mouse isn't over the surface.
        """
        pass

    @abstractmethod
    def process_inputs(self, mouse_position: Point):
        raise NotImplementedError
