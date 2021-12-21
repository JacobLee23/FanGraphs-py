#! usr/bin/env python
# fangraphs/scraper.py

"""

"""

from typing import *

import bs4
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from .selectors import Selectors


def get_soup(html: str) -> bs4.BeautifulSoup:
    """

    :param html:
    :return:
    """
    return bs4.BeautifulSoup(html, features="lxml")


class FanGraphsPage:
    """

    """
    address: str

    path: str
    filter_widgets: dict[str, dict]

    export_data: str = ""

    def __init__(self):
        self.soup = None

        self.selectors = None

    def load_soup(self, html: str) -> None:
        """

        :param html:
        """
        self.soup = get_soup(html)

    def load_selectors(self) -> None:
        """

        """
        if self.soup is None:
            raise NotImplementedError
        self.selectors = Selectors(self.filter_widgets, self.soup)


class _Scraper:
    """

    """
    _address: str = None

    def __init__(self):
        if self._address is None:
            raise NotImplementedError


class SyncScraper:
    """

    """
    def __init__(self, fgpage: FanGraphsPage):
        """
        :param fgpage:
        """
        self.fgpage = fgpage

    def __enter__(self):
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch()
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self.page.goto(self.fgpage.address, timeout=0)

        html = self.page.content()
        self.fgpage.load_soup(html)
        self.fgpage.load_selectors()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__browser.close()
        self.__play.stop()

    def start(self):
        """

        """
        return self.__enter__()

    def stop(self):
        """

        """
        return self.__exit__(None, None, None)

    def widgets(self) -> tuple[str]:
        """

        :return:
        """
        return tuple(self.fgpage.selectors.widgets)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            return widget.options()
        raise Exception  # TODO: Define custom exception

    def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            return widget.current(self.page)
        raise Exception  # TODO: Define custom exception

    def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            widget.configure(self.page, option)
            return
        raise Exception  # TODO: Define custom exception


class AsyncScraper:
    """

    """
    def __init__(self, fgpage: FanGraphsPage):
        """
        :param fgpage:
        """
        self.fgpage = fgpage

    async def __aenter__(self):
        self.__play = await async_playwright().start()
        self.__browser = await self.__play.chromium.launch()
        self.page = await self.__browser.new_page(
            accept_downloads=True
        )
        await self.page.goto(self.fgpage.address, timeout=0)

        html = await self.page.content()
        self.fgpage.load_soup(html)
        self.fgpage.load_selectors()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__browser.close()
        await self.__play.stop()

    async def start(self):
        """

        """
        return await self.__aenter__()

    async def stop(self):
        """

        """
        return await self.__aexit__(None, None, None)

    def widgets(self) -> tuple[bool]:
        """

        :return:
        """
        return tuple(self.fgpage.selectors.widgets)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            return widget.options()
        raise Exception     # TODO: Define custom exception

    async def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            return await widget.acurrent(self.page)
        raise Exception     # TODO: Define custom exception

    async def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        widget = self.fgpage.selectors.widgets.get(wname)
        if widget is not None:
            await widget.aconfigure(self.page, option)
            return
        raise Exception     # TODO: Define custom exception
