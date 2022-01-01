#! usr/bin/env python
# fangraphs/leaders.py

"""

"""

import datetime
import re

import numpy as np
import pandas as pd

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


class GameSpan(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/special/60-game-span"

    filename = "game_span.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ".data-export"

    _dt_format = "%Y-%m-%dT%X"

    def __data(self, raw: pd.DataFrame) -> pd.DataFrame:
        """

        :param raw:
        :return:
        """
        dataframe = raw.copy()

        dataframe["Start Date"] = dataframe["Start Date"].map(
            lambda d: datetime.datetime.strptime(d, self._dt_format)
        )
        dataframe["End Date"] = dataframe["End Date"].map(
            lambda d: datetime.datetime.strptime(d, self._dt_format)
        )

        return dataframe

    def data(self, page) -> pd.DataFrame:
        return self.__data(self.export_data(page))

    async def adata(self, page) -> pd.DataFrame:
        return self.__data(await self.export_data(page))


class International(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/international"

    filename = "international.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ".data-export"

    _regex = re.compile(r"^([A-Za-z\-]+)")

    def __data(self, raw: pd.DataFrame) -> pd.DataFrame:
        dataframe = raw.copy()

        dataframe["Name"] = dataframe["Name"].map(
            lambda n: m.group(1) if (m := self._regex.search(n)) is not None else n
        )

        return dataframe

    def data(self, page) -> pd.DataFrame:
        return self.__data(self.export_data(page))

    async def adata(self, page) -> pd.DataFrame:
        return self.__data(await self.export_data(page))


class MajorLeague(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders.aspx"

    filename = "major_league.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = "#LeaderBoard1_cmdCSV"


class SeasonStat(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/season-stat-grid"

    filename = "season_stat.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ".page-item-control > select"

    def __data(self) -> pd.DataFrame:
        """

        :return:
        """
        table = self.soup.select_one(".table-scroll")
        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe.drop(columns=dataframe.columns[0], inplace=True)
        dataframe.replace("", np.nan, inplace=True)

        return dataframe

    def data(self, page) -> pd.DataFrame:
        return self.__data()

    async def adata(self, page) -> pd.DataFrame:
        return self.__data()


class Splits(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/splits-leaderboards"

    filename = "splits.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ".data-export"


class WAR(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/warleaders.aspx"

    filename = "war.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = "#WARBoard1_cmdCSV"
