#! usr/bin/env python
# fangraphs/scraper.py

"""

"""

import json
from typing import Any, Optional, Union

import bs4
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from . import logger
from . import selectors


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

    export_data_css: str = ""

    _widget_types = {
        "selections": selectors.Selection,
        "dropdowns": selectors.Dropdown,
        "checkboxes": selectors.Checkbox,
        "switches": selectors.Switch
    }

    def __init__(self, html: str):
        """
        :param html:
        """
        with open(self.path, "r", encoding="utf-8") as file:
            self.filter_widgets = json.load(file)

        self.soup = get_soup(html)

        for wname, wclass in self._widget_types.items():
            if (wdict := self.filter_widgets.get(wname)) is not None:
                for attr, kwargs in wdict.items():
                    self.__setattr__(attr, wclass(self.soup, **kwargs))

        self.widgets = self._compile_widgets()

    def _compile_widgets(self) -> dict[str, Any]:
        """

        """
        widgets = {}

        for wtype in list(self._widget_types):
            if (wnames := self.filter_widgets.get(wtype)) is not None:
                logger.debug("Processing filter widget type: %s", wtype)
                for name in wnames:
                    wclass = self.__dict__.get(name)
                    widgets.update({name: wclass})
                    logger.debug("Processed filter widget: %s (%s)", name, wclass)

        return widgets


class SyncScraper:
    """

    """
    def __init__(self, fgpage):
        """
        :param fgpage:
        """
        self.fgpage, self._fgpage = None, fgpage

        self.__play, self.__browser, self.page = None, None, None

    def __enter__(self):
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch()
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self.page.goto(self._fgpage.address, timeout=0)

        html = self.page.content()
        self.fgpage = self._fgpage(html)

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
        return tuple(self.fgpage.widgets)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            return widget.options()
        raise Exception  # TODO: Define custom exception

    def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            return widget.current(self.page)
        raise Exception  # TODO: Define custom exception

    def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            widget.configure(self.page, option)
            return
        raise Exception  # TODO: Define custom exception


class AsyncScraper:
    """

    """
    def __init__(self, fgpage):
        """
        :param fgpage:
        """
        self.fgpage, self._fgpage = None, fgpage

        self.__play, self.__browser, self.page = None, None, None

    async def __aenter__(self):
        self.__play = await async_playwright().start()
        self.__browser = await self.__play.chromium.launch()
        self.page = await self.__browser.new_page(
            accept_downloads=True
        )
        await self.page.goto(self._fgpage.address, timeout=0)

        html = await self.page.content()
        self.fgpage = self._fgpage(html)

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
        return tuple(self.fgpage.widgets)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            return widget.options()
        raise Exception     # TODO: Define custom exception

    async def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            return await widget.acurrent(self.page)
        raise Exception     # TODO: Define custom exception

    async def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        widget = self.fgpage.widgets.get(wname)
        if widget is not None:
            await widget.aconfigure(self.page, option)
            return
        raise Exception     # TODO: Define custom exception
