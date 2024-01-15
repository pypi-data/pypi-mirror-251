# -*- coding: utf-8 -*-

"""
Feature:

User can search folder in a root directory, and then tap "Enter" to enter
a sub query session to search file in the selected folder. At the end, user
can tab "Enter" to open the file using the default application. Also, user can
tap "F1" to exit the sub query session and go back to the folder search session.

Difficulty: Hard

Dependencies:

.. code-block:: bash

    pip install fuzzywuzzy>=0.18.0,<1.0.0
    pip install python-Levenshtein>=0.21.0,<1.0.0

Demo: https://asciinema.org/a/616119
"""

import typing as T
import dataclasses
from pathlib import Path

from fuzzywuzzy import process
import zelfred.api as zf


@dataclasses.dataclass
class OpenFileActionItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        """
        Open file in default application.
        """
        zf.open_file(Path(self.arg))


@dataclasses.dataclass
class CopyFilePathActionItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        """
        Copy file path.
        """
        print(
            f"copied {self.arg!r} path to clipboard (not really copied, just for demo purpose)"
        )


@dataclasses.dataclass
class CopyFileContentActionItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        """
        Copy file content.
        """
        content = Path(self.arg).read_text()
        print(
            f"copied {self.arg!r} file content {content!r} to clipboard (not really copied, just for demo purpose)"
        )


@dataclasses.dataclass
class FileItem(zf.Item):
    """
    Represent a file in the dropdown menu.
    """

    @classmethod
    def from_names(cls, name_list: T.List[str], folder: str) -> T.List["FileItem"]:
        """
        Convert a file name list to a list of items. The file name
        will become the title, uid, autocomplete and the arg.
        """
        return [
            cls(
                uid=name,
                title=name,
                subtitle=f"hit 'Enter' to open this file",
                arg=str(dir_home.joinpath(folder, name)),
                autocomplete=name,
            )
            for name in name_list
        ]

    def enter_handler(self, ui: zf.UI):
        """
        Open file in default application.
        """
        # define the new handler function for the sub query session
        path = Path(self.arg)

        def sub_handler(query: str, ui: zf.UI):
            """
            A partial function that using the given folder.
            """
            return handler_file_action(path, query, ui)

        # run the sub session using the new handler
        # user can tap 'F1' to exit the sub query session,
        # and go back to the folder selection session.
        ui.run_sub_session(handler=sub_handler, initial_query="")


@dataclasses.dataclass
class FolderItem(zf.Item):
    """
    Represent a folder in the dropdown menu.
    """

    @classmethod
    def from_names(cls, name_list: T.List[str]) -> T.List["FolderItem"]:
        """
        Convert a folder name list to a list of items. The folder name
        will become the title, uid, autocomplete and the arg.
        """
        return [
            cls(
                title=name,
                subtitle=f"hit 'Enter' to search file in this folder",
                uid=name,
                autocomplete=name,  # allow user to tap 'Tab' to auto-complete
                arg=name,  # the argument of the folder item will be used to list files
            )
            for name in name_list
        ]

    def enter_handler(self, ui: zf.UI):
        """
        Enter a sub query session.

        .. note::

            THIS IS A VERY GOOD EXAMPLE OF HOW TO ENTER A SUB QUERY SESSION.

            your main UI loop has a handler, sub query session too. So you need
            to define a new handler function for the sub query session, and then
            use the ``ui.run_sub_session()`` method to enter the sub session.
            You can also use ``initial_query`` argument to set the start-up
            input query to display in the line editor.
        """
        # define the new handler function for the sub query session
        folder = self.arg

        def sub_handler(query: str, ui: zf.UI):
            """
            A partial function that using the given folder.
            """
            return handler_file(folder, query, ui)

        # run the sub session using the new handler
        # user can tap 'F1' to exit the sub query session,
        # and go back to the folder selection session.
        ui.run_sub_session(handler=sub_handler, initial_query="")


dir_home = Path(__file__).absolute().parent.joinpath("home")


def handler_file_action(path: Path, query: str, ui: zf.UI):
    """
    This is the handler for the nested sub query (sub query in sub query) session.

    Given a path, you have to create a partial function that using the given
     path. The partial function will become the final handler of the sub query.

    This handler returns couple of action you can do with the file.
    """
    return [
        OpenFileActionItem(
            title="Open file",
            subtitle=f"hit 'Enter' to open file",
            uid="open-file",
            autocomplete=path.name,  # allow user to tap 'Tab' to auto-complete
            arg=str(
                path
            ),  # the argument of OpenFileActionItem will be used to open file
        ),
        CopyFilePathActionItem(
            title="Copy file path",
            subtitle=f"hit 'Enter' to copy file path",
            uid="copy-file-path",
            autocomplete=path.name,  # allow user to tap 'Tab' to auto-complete
            arg=str(
                path
            ),  # the argument of OpenFileActionItem will be used to open file
        ),
        CopyFileContentActionItem(
            title="Copy file content",
            subtitle=f"hit 'Enter' to copy file content",
            uid="copy-file-content",
            autocomplete=path.name,  # allow user to tap 'Tab' to auto-complete
            arg=str(
                path
            ),  # the argument of OpenFileActionItem will be used to open file
        ),
    ]


def handler_file(folder: str, query: str, ui: zf.UI):
    """
    This is the handler for the sub query session.

    Given a folder, you have to create a partial function that using the given
     folder. The partial function will become the final handler of the sub query.
    """
    file_list = [p.name for p in dir_home.joinpath(folder).iterdir()]
    # if query is not empty
    if query:
        # sort by fuzzy match similarity
        results = process.extract(query, file_list, limit=len(file_list))
        return FileItem.from_names([file for file, score in results], folder)
    # if query is empty, return the full list in the original order
    else:
        return FileItem.from_names(file_list, folder)


def handler_folder(query: str, ui: zf.UI):
    """
    This is the handler for folder selection.
    """
    folder_list = [p.name for p in dir_home.iterdir()]
    # if query is not empty
    if query:
        # sort by fuzzy match similarity
        results = process.extract(query, folder_list, limit=len(folder_list))
        return FolderItem.from_names([folder for folder, score in results])
    # if query is empty, return the full list in the original order
    else:
        return FolderItem.from_names(folder_list)


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(handler=handler_folder, capture_error=True)
    ui.run()
