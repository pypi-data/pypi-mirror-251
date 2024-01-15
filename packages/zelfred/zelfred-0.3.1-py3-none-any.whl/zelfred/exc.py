# -*- coding: utf-8 -*-

"""
Zelfred project related Exceptions.
"""

import typing as T


class EndOfInputError(Exception):
    """
    Raises to indicate the UI should exit.
    """

    def __init__(
        self,
        selection: T.Any,
        message: str = "End of input",
        *args,
    ):
        super().__init__(*args)
        self.selection = selection
        self.message = message


class JumpOutSessionError(Exception):
    """
    Raises to indicate that the UI should quit the current session
    (e.g. current handler) and jump out to the previous session (e.g. previous handler).
    """
    pass


JumpOutLoopError = JumpOutSessionError  # this is for backward compatibility


class TerminalTooSmallError(SystemError):
    """
    Raises to indicate that the terminal size is too small to render the UI.
    """
    pass


class NoItemToSelectError(IndexError):
    """
    todo: doc string here
    """
    pass
