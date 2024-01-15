# -*- coding: utf-8 -*-

"""
Feature:

User type query and return a dropdown list of matched Google Chrome bookmarks.
User can tap "Enter" to open it in default web browser.

Difficulty: Medium

Dependencies:

.. code-block:: bash

    pip install sayt==0.6.3

Demo: https://asciinema.org/a/617801
"""

import typing as T
import json
import dataclasses
from pathlib import Path

# we need this to index and search the data
import sayt.api as sayt

# import zelfred public API
import zelfred.api as zf

# define important file paths
dir_home = Path.home()
dir_zelfred = dir_home.joinpath(".zelfred")
dir_root = dir_zelfred.joinpath("app-gallery", "search-google-chrome-bookmark")
dir_root.mkdir(parents=True, exist_ok=True)
dir_index = dir_root.joinpath(".index")
dir_cache = dir_root.joinpath(".cache")


def find_google_chrom_bookmark_file_on_windows() -> Path:
    """
    Locate the Google Chrome bookmark file on Windows.
    """
    path = dir_home.joinpath(
        "AppData",
        "Local",
        "Google",
        "Chrome",
        "User Data",
        "Default",
        "Bookmarks",
    )
    if path.exists():
        return path
    else:
        raise FileNotFoundError


def find_google_chrome_bookmark_file_on_mac() -> Path:
    """
    Locate the Google Chrome bookmark file on MacOS.
    """
    path = dir_home.joinpath(
        "Library",
        "Application Support",
        "Google",
        "Chrome",
        "Default",
        "Bookmarks",
    )
    if path.exists():
        return path
    else:
        raise FileNotFoundError


def find_google_chrome_bookmark_file() -> Path:
    """
    Locate the Google Chrome bookmark file.

    Reference: https://www.howtogeek.com/welcome-to-cybersecurity-awareness-week-2023/
    """
    for func in [
        find_google_chrom_bookmark_file_on_windows,
        find_google_chrome_bookmark_file_on_mac,
    ]:
        try:
            return func()
        except FileNotFoundError:
            pass
    raise FileNotFoundError


@dataclasses.dataclass
class Bookmark:
    """
    Google Chrome bookmark dataclass.
    """

    name: str
    url: str
    name_text: str
    name_ngram: str


def parse_bookmark_file(p: Path) -> T.List[Bookmark]:
    """
    extract list of bookmark object from the bookmark file.
    """
    data = json.loads(p.read_text())
    bookmark_dct = data.get("roots", {}).get("bookmark_bar", {})

    def extract_bookmark(
        node: dict,
        _bookmark_list: T.Optional[T.List[Bookmark]] = None,
    ):
        if _bookmark_list is None:
            _bookmark_list = list()
        for dct in node.get("children", []):
            if "url" in dct:
                name = dct["name"]
                bookmark = Bookmark(
                    name=name,
                    name_text=name,
                    name_ngram=name,
                    url=dct["url"],
                )
                _bookmark_list.append(bookmark)
            else:
                extract_bookmark(dct, _bookmark_list)
        return _bookmark_list

    return extract_bookmark(node=bookmark_dct)


# def downloader():
#     """
#     Return the list of bookmark object for search.
#     """
#     p = find_google_chrome_bookmark_file()
#     bookmark_list = parse_bookmark_file(p)
#     return [dataclasses.asdict(bm) for bm in bookmark_list]


def downloader():
    """
    This function returns dummy data for demo.
    """
    data = [
        ("Google", "https://www.google.com/"),
        ("Facebook", "https://www.facebook.com/"),
        ("Amazon", "https://www.amazon.com/"),
        ("Apple", "https://www.apple.com/"),
        ("Linkedin", "https://www.linkedin.com/"),
        ("Microsoft", "https://www.microsoft.com/"),
    ]
    return [
        dataclasses.asdict(
            Bookmark(
                name=name,
                url=url,
                name_text=name,
                name_ngram=name,
            )
        )
        for name, url in data
    ]


# create the search as you type dataset, it will automatically refresh every 5 minutes
ds = sayt.DataSet(
    dir_index=dir_index,
    index_name="google_chrome_bookmark",
    fields=[
        sayt.TextField("name_text", stored=False),
        sayt.NgramWordsField("name_ngram", minsize=2, maxsize=8),
        sayt.StoredField("name"),
        sayt.StoredField("url"),
    ],
    dir_cache=dir_cache,
    cache_key="google_chrome_bookmark",
    cache_tag="google_chrome_bookmark",
    cache_expire=5 * 60,
    downloader=downloader,
)


@dataclasses.dataclass
class UrlItem(zf.Item):
    """
    Define the custom item class because we need to override the ``enter_handler``.
    """

    @classmethod
    def from_doc(cls, doc: dict):
        return cls(
            title=doc["name"],
            subtitle="hit 'Enter' to open: " + doc["url"],
            uid=doc["url"],
            autocomplete=doc["name"],
            arg=doc["url"],
        )

    def enter_handler(self, ui: zf.UI):
        """
        Open the bookmark in web browser.
        """
        zf.open_url(self.arg)


def handler(query: str, ui: zf.UI):
    """
    The handler is the core of a Zelfred App. It's a user-defined function
    that takes the entered query and the UI object as inputs and returns
    a list of items to render.
    """
    # if query is not empty
    if query:
        docs = ds.search(query)
    # if query is empty, just list first 20 bookmarks
    else:
        docs = ds.search("*")

    # if find matches
    if len(docs):
        return [UrlItem.from_doc(doc) for doc in docs]
    # if no match
    else:
        return [
            UrlItem(
                title="No result found.",
                subtitle="check your data",
                uid="no-result",
            )
        ]


if __name__ == "__main__":
    # reset the debugger and enable it
    zf.debugger.reset()
    zf.debugger.enable()

    # create the UI and run it
    ui = zf.UI(handler=handler, capture_error=False)
    ui.run()
