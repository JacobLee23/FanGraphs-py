#! usr/bin/env python
# fangraphs/depth_charts.py

"""

"""

from typing import Generator

import pandas as pd

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


def _get_table_elements(page, *, css: str = "#content > div > table"):
    """

    :type page: playwright.sync_api._generated.Page
    :param css:
    :return:
    :rtype: list[playwright.sync_api._generated.ElementHandle]
    """
    return page.query_selector_all(css)


async def _aget_table_elements(page, *, css: str = "#content > div > table"):
    """

    :type page: playwright.async_api._generated.Page
    :param css:
    :return:
    :rtype: list[playwright.async_api._generated.ElementHandle]
    """
    return await page.query_selector_all(css)


def _get_table_names(page, *, css: str = "#content > div > a") -> list[str]:
    """

    :type page: playwright.sync_api._generated.Page
    :param css:
    :return:
    """
    return [e.text_content() for e in page.query_selector_all(css)]


async def _aget_table_names(page, *, css: str = "#content > div > a") -> list[str]:
    """

    :type page: playwright.async_api._generated.Page
    :param css:
    :return:
    """
    return [await e.text_content() for e in await page.query_selector_all(css)]


def _get_table_headers(table, *, css: str = "thead > tr > th") -> list[str]:
    """

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    :param css:
    :return:
    """
    return [e.text_content() for e in table.query_selector_all(css)]


async def _aget_table_headers(table, *, css: str = "thead > tr > th") -> list[str]:
    """

    :param table:
    :type table: playwright.async_api._generated.ElementHandle
    :param css:
    :return:
    """
    return [await e.text_content() for e in await table.query_selector_all(css)]


def _get_table_rows(
        table, *, css: str = "tr[class*='depth']"
) -> Generator[tuple[int, list[str]], None, None]:
    """

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    :param css:
    :return:
    """
    for ind, elem in enumerate(table.query_selector_all(css)):
        yield ind, [e.text_content() for e in elem.query_selector_all("td")]


async def _aget_table_rows(
        table, *, css: str = "tr[class*='depth']"
) -> Generator[tuple[int, list[str]], None, None]:
    """

    :param table:
    :type table: playwright.async_api._generated.ElementHandle
    :param css:
    :return:
    """
    for ind, elem in enumerate(await table.query_selector_all(css)):
        yield ind, [await e.text_content() for e in await elem.query_selector_all("td")]


def data(table_names: list[str], table_elems) -> dict[str, pd.DataFrame]:
    """

    :param table_names:
    :param table_elems:
    :type table_elems: list[playwright.sync_api._generated.ElementHandle]
    :return:
    """
    dfdict = {}

    for name, elem in zip(table_names, table_elems):
        dataframe = pd.DataFrame(columns=list(_get_table_headers(elem)))
        for ind, row in _get_table_rows(elem):
            dataframe.loc[ind] = row

        dfdict.setdefault(name, dataframe)

    return dfdict


async def adata(table_names: list[str], table_elems) -> dict[str, pd.DataFrame]:
    """

    :param table_names:
    :param table_elems:
    :type table_elems: list[playwright.async_api._generated.ElementHandle]
    :return:
    """
    dfdict = {}

    for name, elem in zip(table_names, table_elems):
        dataframe = pd.DataFrame(columns=list(await _aget_table_headers(elem)))
        async for ind, row in _aget_table_rows(elem):
            dataframe.loc[ind] = row

        dfdict.setdefault(name, dataframe)

    return dfdict


class __Position(FanGraphsPage):
    """

    """
    def data(self, page) -> dict[str, pd.DataFrame]:
        table_elems = _get_table_elements(page)
        table_names = _get_table_names(page) + ["General"]

        return data(table_names, table_elems)

    async def adata(self, page) -> dict[str, pd.DataFrame]:
        table_elems = await _aget_table_elements(page)
        table_names = await _aget_table_names(page) + ["General"]

        return await adata(table_names, table_elems)


class Standings(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=Standings"

    filename = "standings.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    def data(self, page) -> dict[str, pd.DataFrame]:
        table_elems = _get_table_elements(page)
        table_names = ["General"] + _get_table_names(page)

        return data(table_names, table_elems)

    async def adata(self, page) -> dict[str, pd.DataFrame]:
        table_elems = await _aget_table_elements(page)
        table_names = ["General"] + await _aget_table_names(page)

        return await adata(table_names, table_elems)


class BaseRuns(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=BaseRuns"

    filename = "baseruns.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    def data(self, page) -> dict[str, pd.DataFrame]:
        table_elems = _get_table_elements(page)
        table_names = ["General"] + _get_table_names(page)

        return data(table_names, table_elems)

    async def adata(self, page) -> dict[str, pd.DataFrame]:
        table_elems = await _aget_table_elements(page)
        table_names = ["General"] + await _aget_table_names(page)

        return await adata(table_names, table_elems)


class DepthCharts(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=ALL&teamid=1"

    filename = "depth_charts.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PC(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=C"

    filename = "p_c.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class P1B(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=1B"

    filename = "p_1b.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class P2B(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=2B"

    filename = "p_2b.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PSS(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=SS"

    filename = "p_ss.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class P3B(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=3B"

    filename = "p_3b.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PLF(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=LF"

    filename = "p_lf.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PCF(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=CF"

    filename = "p_cf.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PRF(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=RF"

    filename = "p_rf.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PSP(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=SP"

    filename = "p_sp.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PRP(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=RP"

    filename = "p_rp.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PDH(__Position):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=DH"

    filename = "p_dh.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class Totals(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/depthcharts.aspx?position=C"

    filename = "totals.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    def data(self, page) -> pd.DataFrame:
        table_elem = page.query_selector(
            "#content > div.depth-charts-aspx_table > table"
        )

        dataframe = pd.DataFrame(columns=list(_get_table_headers(table_elem)))
        for ind, row in _get_table_rows(table_elem):
            dataframe.loc[ind] = row

        return dataframe

    async def adata(self, page) -> pd.DataFrame:
        table_elem = await page.query_selector(
            "#content > div.depth-charts-aspx_table > table"
        )

        dataframe = pd.DataFrame(columns=list(await _aget_table_headers(table_elem)))
        async for ind, row in _aget_table_rows(table_elem):
            dataframe.loc[ind] = row

        return dataframe
