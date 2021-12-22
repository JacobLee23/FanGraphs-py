#! usr/bin/env python
# fangraphs/scraper.py

"""

"""

import json
import os
from typing import Any, NamedTuple, Optional, Union

import bs4
import pandas as pd
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from . import logger
from . import selectors


def load_soup(html: str) -> bs4.BeautifulSoup:
    """

    :param html:
    :return:
    """
    return bs4.BeautifulSoup(html, features="lxml")


def load_filter_queries(path) -> dict:
    """
    
    :param path: 
    :return: 
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


class FanGraphsPage:
    """

    """
    address: str

    path: str
    filter_queries: dict

    export_data_css: str = ""

    _query_types = {
        "selections": selectors.Selection,
        "dropdowns": selectors.Dropdown,
        "checkboxes": selectors.Checkbox,
        "switches": selectors.Switch
    }

    class TableData(NamedTuple):
        """

        """
        dataframe: pd.DataFrame
        row_elems: bs4.ResultSet
        header_elems: bs4.ResultSet

    def __init__(self, html: str):
        """
        :param html:
        """
        self.soup = load_soup(html)

        for qname, qclass in self._query_types.items():
            if (qdict := self.filter_queries.get(qname)) is not None:
                for attr, kwargs in qdict.items():
                    self.__setattr__(attr, qclass(self.soup, **kwargs))

        self.queries = self.compile_queries()

    def compile_queries(self) -> dict[str, Any]:
        """

        """
        queries = {}

        for qtype in list(self._query_types):
            if (qnames := self.filter_queries.get(qtype)) is not None:
                logger.debug("Processing filter query type: %s", qtype)
                for name in qnames:
                    qclass = self.__dict__.get(name)
                    queries.update({name: qclass})
                    logger.debug("Processed filter query: %s (%s)", name, qclass)

        return queries

    @staticmethod
    def close_banner_ad(page) -> None:
        """

        :type page: playwright.sync_api._generated.Page
        """
        if page.query_selector_all("#ezmob-wrapper > div[style='display: none;']"):
            return

        elem = page.query_selector(".ezmob-footer-close")
        if elem:
            elem.click()

    @staticmethod
    async def aclose_banner_ad(page) -> None:
        """

        :type page: playwright.async_api._generated.Page
        """
        if await page.query_selector_all("#ezmob-wrapper > div[style='display: none;']"):
            return

        elem = await page.query_selector(".ezmob-footer-close")
        if elem:
            await elem.click()

    def export_data(self, page) -> pd.DataFrame:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        self.close_banner_ad(page)
        with page.expect_download() as down_info:
            page.click(self.export_data_css)

        download = down_info.value
        download_path = download.path()
        dataframe = pd.read_csv(download_path)
        os.remove(download_path)

        return dataframe

    async def aexport_data(self, page) -> pd.DataFrame:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        await self.aclose_banner_ad(page)
        async with page.expect_download() as down_info:
            await page.click(self.export_data_css)

        download = await down_info.value
        download_path = await download.path()
        dataframe = pd.read_csv(download_path)
        os.remove(download_path)

        return dataframe

    def data(self, page) -> Any:
        """

        :type page: playwright.sync_api._generated.Page
        :return:
        """
        return self.export_data(page)

    async def adata(self, page) -> Any:
        """

        :type page: playwright.async_api._generated.Page
        :return:
        """
        return await self.aexport_data(page)

    def scrape_table(self, table: bs4.Tag, *, css_h: str = "thead > tr", css_r: str = "tbody > tr") -> TableData:
        """

        :param table:
        :param css_h:
        :param css_r:
        :return:
        """
        header_elems = table.select_one(css_h).select("th")
        row_elems = table.select(css_r)

        dataframe = pd.DataFrame(
            data=[[e.text for e in r.select("td")] for r in row_elems],
            columns=[e.text for e in header_elems]
        )

        table_data = self.TableData(dataframe, row_elems, header_elems)

        return table_data


class SyncScraper:
    """

    """
    def __init__(self, fgpage):
        """
        :param fgpage:
        """
        self._fgpage = fgpage

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

    def queries(self) -> tuple[str]:
        """

        :return:
        """
        return tuple(self.fgpage.queries)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            return query.options()
        raise Exception  # TODO: Define custom exception

    def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            return query.current(self.page)
        raise Exception  # TODO: Define custom exception

    def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            query.configure(self.page, option)
            return
        raise Exception  # TODO: Define custom exception

    def data(self) -> Any:
        """

        :return:
        """
        return self.fgpage.data(self.page)


class AsyncScraper:
    """

    """
    def __init__(self, fgpage):
        """
        :param fgpage:
        """
        self._fgpage = fgpage

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

    def queries(self) -> tuple[bool]:
        """

        :return:
        """
        return tuple(self.fgpage.queries)

    def options(self, wname: str) -> Optional[tuple[Union[str, bool]]]:
        """

        :param wname:
        :return:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            return query.options()
        raise Exception     # TODO: Define custom exception

    async def current(self, wname: str) -> Optional[Union[str, bool]]:
        """

        :param wname:
        :return:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            return await query.acurrent(self.page)
        raise Exception     # TODO: Define custom exception

    async def configure(self, wname: str, option: Union[str, bool]) -> None:
        """

        :param wname:
        :param option:
        """
        query = self.fgpage.queries.get(wname)
        if query is not None:
            await query.aconfigure(self.page, option)
            return
        raise Exception     # TODO: Define custom exception

    async def data(self) -> Any:
        """

        :return:
        """
        return await self.fgpage.adata(self.page)
