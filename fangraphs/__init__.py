#! usr/bin/env python
# fangraphs/__init__.py

"""

"""

from typing import *

import bs4
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from .logger import logger


def get_soup(html: str) -> bs4.BeautifulSoup:
    """

    :param html:
    :return:
    """
    return bs4.BeautifulSoup(html, features="lxml")


class SyncScraper:
    """

    """
    _address: str = None

    def __init__(self):
        if self._address is None:
            raise NotImplementedError

        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch()
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self.page.goto(self._address, timeout=0)

        self.soup = get_soup(self.page.content())

    def __del__(self):
        self.__browser.close()
        self.__play.stop()


class AsyncScraper:
    """

    """
    _address: str = None

    def __init__(self):
        if self._address is None:
            raise NotImplementedError

        self.__play = await async_playwright().start()
        self.__browser = await self.__play.chromium.launch()
        self.page = await self.__browser.new_page(
            accept_downloads=True
        )
        await self.page.goto(self._address, timeout=0)

        self.soup = get_soup(await self.page.content())

    def __del__(self):
        self.__browser.close()
        self.__play.stop()
