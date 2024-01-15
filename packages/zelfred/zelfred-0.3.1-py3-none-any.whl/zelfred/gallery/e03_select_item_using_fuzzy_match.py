# -*- coding: utf-8 -*-

"""
Feature:

Use the user input to sort a list of items by fuzzy match similarity.
Allow user to tap "Enter" to copy the content to clipboard.

Dependencies:

.. code-block:: bash

    pip install fuzzywuzzy>=0.18.0,<1.0.0
    pip install python-Levenshtein>=0.21.0,<1.0.0
    pip install pyperclip>=1.8.0,<2.0.0

Demo: https://asciinema.org/a/617874
"""

import dataclasses

# we need this library to copy text to clipboard
import pyperclip

# we need this library to do fuzzy match
from fuzzywuzzy import process

# import zelfred public API
import zelfred.api as zf


@dataclasses.dataclass
class Item(zf.Item):
    """
    The default ``zf.Item`` does not implement any user action handler methods.
    To copy the password to the clipboard when the user taps "Enter," we need to
    define a custom item class and override the ``enter_handler`` method."

    By default, the UI can perform a "user action" when the following keys are tapped:

    - Enter
    - Ctrl A
    - Ctrl W
    - Ctrl U
    - Ctrl P

    When user taps one of these keys, the UI will call the corresponding handler method
    and exit immediately.
    """

    def enter_handler(self, ui: zf.UI):
        """
        Copy the content to clipboard.
        """
        pyperclip.copy(self.arg)


def create_item(text: str, ui: zf.UI) -> Item:
    """
    A helper function to create an item from text.
    """
    return Item(
        title=text,
        # the ui.terminal is a blessed.Terminal object,
        # we can use it to add syntax highlight to the text.
        # you can find more information at https://blessed.readthedocs.io/en/latest/colors.html
        subtitle=f"hit {ui.terminal.magenta}Enter{ui.terminal.normal} to copy to clipboard",
        # uid is a unique identifier of the item for internal deduplication
        # if you don't specify it, it will be generated automatically
        uid=text,
        # user can tap "Tab" to autocomplete the query
        autocomplete=text,
        # the argument of the item will be used to copy to clipboard
        arg=text,
    )


zen_of_python = [
    "Beautiful is better than ugly.",
    "Explicit is better than implicit.",
    "Simple is better than complex.",
    "Complex is better than complicated.",
    "Flat is better than nested.",
    "Sparse is better than dense.",
    "Readability counts.",
    "Special cases aren't special enough to break the rules.",
    "Although practicality beats purity.",
    "Errors should never pass silently.",
    "Unless explicitly silenced.",
    "In the face of ambiguity, refuse the temptation to guess.",
    "There should be one-- and preferably only one --obvious way to do it.",
    "Although that way may not be obvious at first unless you're Dutch.",
    "Now is better than never.",
    "Although never is often better than *right* now.",
    "If the implementation is hard to explain, it's a bad idea.",
    "If the implementation is easy to explain, it may be a good idea.",
    "Namespaces are one honking great idea -- let's do more of those!",
]


def handler(query: str, ui: zf.UI):
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    # if query is not empty
    if query:
        # sort by fuzzy match similarity
        # you can find more information at: https://github.com/seatgeek/fuzzywuzzy
        results = process.extract(query, zen_of_python, limit=len(zen_of_python))
        return [create_item(text, ui) for text, score in results]
    # if query is empty, return the full list in the original order
    else:
        return [create_item(text, ui) for text in zen_of_python]


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(
        # tell the UI to use the handler function
        handler=handler,
        # capture error and display debug information in the UI,
        # this is the default behavior, if this is set to False, then it will
        # raise Exception and stop the program.
        capture_error=True,
    )
    # run the UI
    ui.run()
