# -*- coding: utf-8 -*-

"""
Feature:

The user types a query and receives a dropdown list of Google search suggestions.
The user can then tap "Enter" to perform a Google search in their web browser.

Difficulty: Medium

Dependencies:

.. code-block:: bash

    pip install requests

Demo: https://asciinema.org/a/616014
"""

import typing as T
import dataclasses

# we need this to parse google search API response
import xml.etree.ElementTree as ET

# we need this to send HTTP request
import requests
import zelfred.api as zf


@dataclasses.dataclass
class Item(zf.Item):
    def enter_handler(self, ui: zf.UI):
        """
        Open the url in default web browser.
        """
        zf.open_url(self.arg)


def encode_query(query: str) -> str:
    """
    Encode the query to be used in the url.
    """
    return query.replace(" ", "+")


class GoogleComplete:
    """
    Google complete API caller and parser.
    """

    google_complete_endpoint = (
        "https://www.google.com/complete/search?output=toolbar&q={query}"
    )

    def _encode_endpoint(self, query: str) -> str:
        """
        :return: full api url.
        """
        query = "+".join([s for s in query.split(" ") if s.strip()])
        return self.google_complete_endpoint.format(query=query)

    def _parse_response(self, html: str) -> T.List[str]:
        """
        :return: list of suggestions.
        """
        root = ET.fromstring(html)
        suggestion_list = list()
        for suggestion in root.iter("suggestion"):
            suggestion_list.append(suggestion.attrib["data"])
        return suggestion_list

    def get(self, query: str) -> T.List[str]:
        """
        :return: list of suggestions.
        """
        url = self._encode_endpoint(query)
        html = requests.get(url).text
        suggestion_list = self._parse_response(html)
        return suggestion_list


google_complete = GoogleComplete()


def handler(query: str, ui: zf.UI):
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    # if query is empty, return the full list in the original order
    if bool(query) is False:
        return [
            Item(
                title="type something to search in google",
            )
        ]
    # if query is not empty
    else:
        suggestion_list = google_complete.get(query)
        return [
            Item(
                title=s,
                subtitle=f"hit 'Enter' to Google search {s!r} in web browser",
                uid=s,
                autocomplete=s,
                # store google search url in arg, so we can access it in enter_handler
                arg=f"https://www.google.com/search?q={encode_query(s)}",
            )
            for s in suggestion_list
        ]


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(handler=handler, capture_error=True)
    ui.run()
