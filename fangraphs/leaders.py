#! usr/bin/env python
# fangraphs/leaders.py

"""

"""

import datetime
import os
import re

import numpy as np
import pandas as pd

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


PATH = os.path.join("fangraphs", "data", "leaders")


class GameSpan(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/special/60-game-span"

    path = os.path.join(PATH, "game_span.json")
    filter_queries = load_filter_queries(path)

    export_data_css = ".data-export"

    @staticmethod
    def __revise_dates(date: str, dt_format="%Y-%m-%dT%X") -> datetime.datetime:
        return datetime.datetime.strptime(date, dt_format)

    def data(self, page) -> pd.DataFrame:
        dataframe = self.export_data(page)

        dataframe["Start Date"] = dataframe["Start Date"].map(self.__revise_dates)
        dataframe["End Date"] = dataframe["End Date"].map(self.__revise_dates)

        return dataframe

    async def adata(self, page) -> pd.DataFrame:
        dataframe = await self.export_data(page)

        dataframe["Start Date"] = dataframe["Start Date"].map(self.__revise_dates)
        dataframe["End Date"] = dataframe["End Date"].map(self.__revise_dates)

        return dataframe


class International(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/international"

    path = os.path.join(PATH, "international.json")
    filter_queries = load_filter_queries(path)

    export_data_css = ".data-export"

    @staticmethod
    def __revise_names(name: str) -> str:
        if (match := re.search(r"^([A-Za-z\-]+)", name)) is not None:
            return match.group(1)
        return name

    def data(self, page) -> pd.DataFrame:
        dataframe = self.export_data(page)

        dataframe["Name"] = dataframe["Name"].map(self.__revise_names)

        return dataframe

    async def adata(self, page) -> pd.DataFrame:
        dataframe = await self.export_data(page)

        dataframe["Name"] = dataframe["Name"].map(self.__revise_names)

        return dataframe


class MajorLeague(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders.aspx"

    path = os.path.join(PATH, "major_league.json")
    filter_queries = load_filter_queries(path)

    export_data_css = "#LeaderBoard1_cmdCSV"


class SeasonStat(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/season-stat-grid"

    path = os.path.join(PATH, "season_stat.json")
    filter_queries = load_filter_queries(path)

    export_data_css = ".page-item-control > select"

    def data(self, page) -> pd.DataFrame:
        table = self.soup.select_one(".table-scroll")
        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe.drop(columns=dataframe.columns[0], inplace=True)
        dataframe.replace("", np.nan, inplace=True)

        return dataframe

    async def adata(self, page) -> pd.DataFrame:
        return self.data(page)


class Splits(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/leaders/splits-leaderboards"

    path = os.path.join(PATH, "splits.json")
    filter_queries = load_filter_queries(path)

    export_data_css = ".data-export"


class WAR(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/warleaders.aspx"

    path = os.path.join(PATH, "war.json")
    filter_queries = load_filter_queries(path)

    export_data_css = "#WARBoard1_cmdCSV"
