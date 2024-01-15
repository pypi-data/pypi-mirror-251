# -*- coding: utf-8 -*-

"""
Feature:

Copy JSON text to clipboard, then hit 'Enter' to dump the formatted JSON to
``${HOME}/tmp/formatted.json`` and automatically open it.

Difficulty: Easy

Dependencies: NA

Demo: https://asciinema.org/a/123456
"""

import json
import dataclasses
from pathlib import Path

import pyperclip
import zelfred.api as zf

p = Path.home().joinpath("tmp", "formatted.json")
p.parent.mkdir(exist_ok=True)


@dataclasses.dataclass
class JsonFormatterItem(zf.Item):
    """
    Represent a json formatter item in the dropdown menu.
    """

    def enter_handler(self, ui: zf.UI):
        """
        Read json from clipboard, format it, write to ~/tmp/formatted.json, then open it.
        """
        s = pyperclip.paste()
        p.write_text(json.dumps(json.loads(s), indent=4))
        zf.open_file(p)


def handler(query: str, ui: zf.UI):
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    return [
        JsonFormatterItem(
            title=f"Hit 'Enter' to format your JSON",
            subtitle="hint: copy your JSON to clipboard before you hit 'Enter'",
        )
    ]


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(handler=handler, capture_error=True)
    ui.run()
