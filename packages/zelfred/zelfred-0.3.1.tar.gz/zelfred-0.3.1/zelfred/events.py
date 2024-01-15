# -*- coding: utf-8 -*-

"""
Keyboard events.
"""

import typing as T
import readchar


class Event:
    pass


class KeyPressedEvent(Event):
    def __init__(self, value):
        self.value = value


class RepaintEvent(Event):
    pass


class KeyEventGenerator:
    """
    Capture keyboard event.
    """
    def __init__(
        self,
        key_generator: T.Optional[T.Callable[[], str]] = None,
    ):
        self._key_generator = key_generator or readchar.readkey

    def next(self) -> KeyPressedEvent:
        """
        Return the next key pressed event.
        """
        return KeyPressedEvent(value=self._key_generator())
