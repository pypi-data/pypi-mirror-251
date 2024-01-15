# -*- coding: utf-8 -*-

"""
Feature:

The user enters (or paste) the absolute path of the file, and the UI generates
a few checksum algorithm options, then user can choose one and hit "Enter" to
copy the checksum value of the selected algorithm. The UI will stay and user can
continue to choose another algorithm and hit "Enter" again.

Difficulty: Easy

Dependencies:

.. code-block:: bash

    pip install pyperclip>=1.8.0,<2.0.0

Demo: https://asciinema.org/a/617871
"""

import typing as T
import hashlib
import dataclasses
from pathlib import Path

# we need this library to copy text to clipboard
import pyperclip

# import zelfred public API
import zelfred.api as zf


# implement the checksum calculator
def md5_of_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def sha1_of_file(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha512_of_file(path: Path) -> str:
    return hashlib.sha512(path.read_bytes()).hexdigest()


algorithms = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
]

algorithm_to_function_mapper = {
    "md5": md5_of_file,
    "sha1": sha1_of_file,
    "sha256": sha256_of_file,
    "sha512": sha512_of_file,
}


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

    When the user taps one of these keys, the UI calls the corresponding
    handler method and exits immediately. To modify this behavior, we can
    override the ``post_enter_handler`` method, which is invoked after the
    ``enter_handler`` method."
    """

    def enter_handler(self, ui: zf.UI):
        """
        Copy the checksum of the file to clipboard.

        The path of the file is stored in the ``self.variables["path"]``.
        The checksum algorithm is stored in the ``self.variables["algo"]``.
        """
        path = Path(self.variables["path"])
        algo = self.variables["algo"]
        checksum = algorithm_to_function_mapper[algo](path)
        pyperclip.copy(checksum)

    def post_enter_handler(self, ui: zf.UI):
        """
        We would like to keep the UI displayed after the user hits 'Enter'.
        Typically, any user input change will trigger the UI to re-render
        and then wait for the next user input. The 'UI.wait_next_user_input()'
        method allows you to skip the re-rendering and wait for the next user input."
        """
        ui.wait_next_user_input()


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
                title="Enter the absolute path of the file ...",
                subtitle="for example: ${HOME}/.zshrc",
                # since my demo is running on macOS, I use the ${HOME}/.zshrc file
                # as an example, you can change it to any file you want.
                autocomplete=str(Path.home().joinpath(".zshrc")),
            )
        ]
    else:
        path = Path(query)
        # if the path does not exist, user might be still typing,
        # so we just display a helper text
        if path.exists() is False:
            return [
                Item(
                    title="Keep entering ...",
                    subtitle=f"{path} doesn't exists.",
                )
            ]
        # if the path is a directory, we display a helper text
        elif path.is_dir():
            return [
                Item(
                    title="🔴 We cannot calculate checksum for a directory!",
                    subtitle=f"{path} is a directory.",
                )
            ]
        # if the path is a file, we display the checksum options
        elif path.is_file():
            return [
                Item(
                    title=f"{algo} of {path}",
                    # the ui.terminal is a blessed.Terminal object,
                    # we can use it to add syntax highlight to the text.
                    # you can find more information at https://blessed.readthedocs.io/en/latest/colors.html
                    subtitle=f"tap {ui.terminal.magenta}Enter{ui.terminal.normal} to copy this checksum to clipboard.",
                    variables={
                        "path": f"{path}",
                        "algo": algo,
                    },
                )
                for algo in algorithms
            ]
        else:  # this should never happen, but just in case
            raise NotImplementedError


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
