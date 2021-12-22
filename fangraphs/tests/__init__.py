#! usr/bin/env python
# fangraphs/tests/__init__.py

"""

"""

import os
import json
from urllib.request import urlopen

import bs4
from playwright.sync_api import sync_playwright


QTYPES = (
    "selections", "dropdowns", "checkboxes", "switches"
)


def get_soup(address: str) -> bs4.BeautifulSoup:
    """

    :param address:
    :return:
    """
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page()
        page.goto(address, timeout=0)
        soup = bs4.BeautifulSoup(page.content(), features="lxml")
        browser.close()
    return soup


class BaseTests:
    """

    """
    @staticmethod
    def _test_address(address: str) -> None:
        """

        :param address:
        """
        assert urlopen(address).code == 200

    @staticmethod
    def _test_path(path: str) -> None:
        """

        :param path:
        """
        assert os.path.exists(path)

    @staticmethod
    def _test_file_contents(path: str) -> None:
        """

        :param path:
        """
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        assert data

        assert isinstance(data, dict)
        assert all(k in QTYPES for k in data)
        assert all(isinstance(v, dict) for v in data.values())
        assert all(isinstance(v, dict) for k in data for v in data[k].values())
        assert all(isinstance(v, (str, list)) for k in data for k_ in data[k] for v in data[k][k_].values())
        assert all(isinstance(e, str) for k in data for k_ in data[k] for v in data[k][k_] for e in v if isinstance(v, list))

    @staticmethod
    def _test_selector(soup: bs4.BeautifulSoup, css: str) -> None:
        """

        :param soup:
        :param css:
        """
        assert len(soup.select(css)) == 1

    @staticmethod
    def _test_selectors(soup: bs4.BeautifulSoup, css: list[str]) -> None:
        """

        :param soup:
        :param css:
        """
        assert all(len(soup.select(c)) == 1 for c in css)
