# -*- coding: utf-8 -*-

"""
Feature:

The user enters the length of the password, and the UI generates a few random passwords
for the user to choose from. The user can tap "Enter" to copy the selected password
to the clipboard, and the UI will exit.

Difficulty: Easy

Dependencies:

.. code-block:: bash

    pip install pyperclip>=1.8.0,<2.0.0

Demo: https://asciinema.org/a/617869
"""

import typing as T
import string
import random
import dataclasses

# we need this library to copy text to clipboard
import pyperclip

# import zelfred public API
import zelfred.api as zf


# implement the random password generator
def remove_chars(chars: str, to_remove: str) -> str:
    for c in to_remove:
        chars = chars.replace(c, "")
    return chars


to_remove = "iIlLoO1O"  # we don't use these chars because they are easily confused

charset_lower = remove_chars(string.ascii_lowercase, to_remove)
charset_upper = remove_chars(string.ascii_uppercase, to_remove)
charset_digits = remove_chars(string.digits, to_remove)
charset_symbol = "!@#$%^&*()_+"
charset = charset_lower + charset_upper + charset_digits + charset_symbol


def random_password(length: int) -> str:
    # first char must be a letter
    first = random.choice(charset_lower + charset_upper)
    # must have at least 1-2 digits, 1-2 uppercase, 1-2 lowercase, 1-2 symbol
    digits = random.choices(charset_digits, k=random.randint(1, 2))
    upper = random.choices(charset_upper, k=random.randint(1, 2))
    lower = random.choices(charset_lower, k=random.randint(1, 2))
    symbol = random.choices(charset_symbol, k=random.randint(1, 2))
    # the rest can be anything
    k = length - 1 - len(digits) - len(upper) - len(lower) - len(symbol)
    if k:
        rest = random.choices(charset, k=k)
    else:
        rest = []
    tail = digits + upper + lower + symbol + rest
    random.shuffle(tail)
    return first + "".join(tail)


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


def handler(query: str, ui: zf.UI) -> T.List[Item]:
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    # if query is empty, display helper text
    if bool(query) is False:
        return [
            Item(
                title="Enter the length of the password ...",
                subtitle="for example: 12",
                # user can tap "Tab" to autocomplete the query
                # we would like to generate a password with length 12 in most of the case
                # so we set the autocomplete to 12
                autocomplete="12",
            )
        ]
    else:
        # try to convert the query into an integer
        try:
            length = int(query)
            # if the length is less than 10, display helper text
            if length < 10:
                return [
                    Item(
                        title=f"We don't support password length less than 10.",
                        subtitle="please enter a number greater than 10!",
                    )
                ]
            # if the length is valid, then generate some passwords
            else:
                items = list()
                for _ in range(20):
                    pwd = random_password(length)
                    item = Item(
                        # the first line of the item in the UI, usually the content of the item.
                        # the ui.terminal is a blessed.Terminal object,
                        # we can use it to add syntax highlight to the text.
                        # you can find more information at https://blessed.readthedocs.io/en/latest/colors.html
                        title=f"{ui.terminal.cyan}{pwd}{ui.terminal.normal}",
                        # the second line of the item in the UI, usually some helper text.
                        subtitle=f"tap {ui.terminal.magenta}Enter{ui.terminal.normal} to copy this password to clipboard",
                        # the argument of the item will be used to copy to clipboard
                        arg=pwd,
                    )
                    items.append(item)
                return items
        # if the query is not a valid integer, display helper text
        except ValueError:
            return [
                Item(
                    title=f"{query!r} is not a valid length.",
                    subtitle="please enter an integer!",
                )
            ]


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
