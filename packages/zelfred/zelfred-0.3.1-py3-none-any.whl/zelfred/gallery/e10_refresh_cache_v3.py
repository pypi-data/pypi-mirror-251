# -*- coding: utf-8 -*-

"""
Feature:

No matter what user entered, always return a random value between 1 and 100.
And this value is based on cache that won't change while user is typing.
However, we want to provide a way to refresh the value. User can type "!~",
then the value will be refreshed after 1 seconds, and the "!~" will be removed
automatically. During the waiting, it will show a helper text to tell user to wait.

Difficulty: Medium

Dependencies: NA

Demo: https://asciinema.org/a/631335
"""

import time
import random

import zelfred.api as zf


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
        # show a helper text
        items = [
            zf.Item(
                title=f"Let's wait 1 seconds for refreshing",
                subtitle="please don't type anything",
            )
        ]
        # explicitly set the items
        ui.run_handler(items=items)
        ui.repaint()
        # run the refresh logic, it may take a while
        time.sleep(1)
        # refresh the value
        cache.value = random.randint(1, 100)
        # remove the "!~" from the query in the UI
        ui.line_editor.press_backspace(2)
        return [
            zf.Item(
                title=f"Value {cache.value}",
                subtitle=f"Type !~ to refresh the value",
            )
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
