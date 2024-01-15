# -*- coding: utf-8 -*-

"""
Feature:

No matter what user entered, always return a random value between 1 and 100.
And this value is based on cache that won't change while user is typing.
However, we want to provide a way to refresh the value. User can type "!~"
and then hit ENTER to refresh the value. When user hit ENTER, it automatically
removes the "!~" part and recover the original query.

Difficulty: Hard

Dependencies: NA

Demo: https://asciinema.org/a/631197
"""

import random
import dataclasses

import zelfred.api as zf


@dataclasses.dataclass
class RefreshItem(zf.Item):
    """
    Represent an item that can refresh cache in the dropdown menu.
    """

    def enter_handler(self, ui: zf.UI):
        """
        Copy the content to clipboard.
        """
        cache.value = None

    def post_enter_handler(self, ui: zf.UI):
        """
        After the user input action, we would like to repaint the dropdown menu
        only to show the "Copied" item, and then wait for the next user input.
        """
        ui.line_editor.move_to_end()
        ui.line_editor.press_backspace(self.variables["n_backspace"])


class Cache:
    def __init__(self):
        self.value = None


cache = Cache()


def handler(query: str, ui: zf.UI):
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    # if query is for refresh value
    if "!~" in query:
        before_query, after_query = query.split("!~", 1)
        return [
            RefreshItem(
                title="Refresh value",
                subtitle=f"Hit {ui.render.ENTER} to refresh the value",
                variables={"n_backspace": len(after_query) + 2},
            ),
        ]
    # otherwise, always return a random value, and cache it
    else:
        if cache.value is None:
            cache.value = random.randint(1, 100)
        return [
            zf.Item(
                title=f"Value {cache.value}",
                subtitle=f"Type !~ to refresh the value",
            )
        ]


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(handler=handler, capture_error=True)
    ui.run()
