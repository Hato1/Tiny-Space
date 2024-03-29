from __future__ import annotations

import random
from pathlib import Path
from typing import Type

import pygame as pg


class ResourceMeta(type):
    def __repr__(self):
        return self.__name__


class Resource(metaclass=ResourceMeta):

    RESOURCE_REGISTRY: list[Type[Resource]] = []

    @classmethod
    def image(cls):
        return pg.image.load(cls.get_file)

    @classmethod
    def get_file(cls) -> Path:
        file = Path(f"assets/resources/{cls}.png")
        assert file.exists(), f"Could not find resource: {file!r}"
        return file

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.RESOURCE_REGISTRY.append(cls)  # Add class to registry.


class Iron(Resource):
    pass


class Oil(Resource):
    pass


class Crystal(Resource):
    pass


class Aerofoam(Resource):
    pass


class ResourceQueue:
    def __init__(self):
        # Comment this out for actual random.
        random.seed("debug")
        self.queue: list[Type[Resource]] = []
        self.extend_queue()

    def extend_queue(self):
        """Repopulates the queue with an even balance of resources."""
        pool = [resource for resource in Resource.RESOURCE_REGISTRY for _ in range(5)]
        random.shuffle(pool)
        self.queue.extend(pool)

    def peek_n(self, n) -> list[Type[Resource]]:
        """Peek, but don't remove the next n items from the queue"""
        while len(self.queue) < n:
            self.extend_queue()
        return self.queue[:n]

    def peek(self):
        """Peek, but don't remove the next item from the queue"""
        return self.peek_n(1)[0]

    def take_n(self, n) -> list[Type[Resource]]:
        """Take the next n resources from the queue"""
        try:
            return self.peek_n(n)
        finally:
            self.queue = self.queue[n:]

    def take(self):
        """Take the next item from the queue"""
        return self.take_n(1)[0]


Queue = ResourceQueue()

if __name__ == "__main__":
    assert "Iron" in [str(r) for r in Resource.RESOURCE_REGISTRY]
