#! usr/bin/env python
# fangraphs/teams.py

"""

"""

import datetime
import re
from typing import Generator, NamedTuple

import bs4
import pandas as pd
import numpy as np

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


class _TeamDepthChart(NamedTuple):
    """

    """
    p_RP: pd.DataFrame
    p_SP: pd.DataFrame

    p_C: pd.DataFrame
    p_1B: pd.DataFrame
    p_2B: pd.DataFrame
    p_3B: pd.DataFrame
    p_SS: pd.DataFrame
    p_LF: pd.DataFrame
    p_CF: pd.DataFrame
    p_RF: pd.DataFrame
    p_DH: pd.DataFrame


class _BattingDepthChart(NamedTuple):
    """

    """
    p_C: pd.DataFrame
    p_1B: pd.DataFrame
    p_2B: pd.DataFrame
    p_SS: pd.DataFrame
    p_3B: pd.DataFrame
    p_LF: pd.DataFrame
    p_CF: pd.DataFrame
    p_RF: pd.DataFrame
    p_DH: pd.DataFrame
    p_ALL: pd.DataFrame


class _PitchingDepthChart(NamedTuple):
    """

    """
    p_SP: pd.DataFrame
    p_RP: pd.DataFrame
    p_ALL: pd.DataFrame


def _stat_table(soup: bs4.BeautifulSoup, name: str) -> bs4.Tag:
    """

    :param soup:
    :param name:
    :return:
    """
    table_elems = soup.select(".team-stats-table")
    table_names = (e.text.title() for e in soup.select("h2.team-header"))

    return next(
        filter(
            lambda n: n[1] == name, zip(table_elems, table_names)
        )
    )[0]


def _scrape_depth_chart(soup: bs4.BeautifulSoup) -> _TeamDepthChart:
    """

    :param soup:
    :return:
    """
    depth_chart_data = []

    position_elems = (
        soup.select_one(f"g#pos{i}") for i in range(11)
    )
    for ind, pos_elem in enumerate(position_elems):
        position = pos_elem.select_one(f"text#pos-label{ind}").text

        players = []
        for elems in zip(
                pos_elem.select("text.player-name"), pos_elem.select("text.player-stat")
        ):
            if not all(e.text for e in elems):
                continue
            try:
                player_id = re.search(
                    r"playerid=(.*)", elems[0].select_one("a").attrs.get("xlink:href")
                ).group(1)
            except AttributeError:
                player_id = None
            players.append([elems[0].text, elems[1].text, player_id])

        dataframe = pd.DataFrame(
            data=players, columns=["Name", "Stat", "PlayerID"]
        )
        dataframe.rename(index=lambda i: i + 1, inplace=True)
        depth_chart_data.append((f"p_{position}", dataframe))

    return _TeamDepthChart(**dict(depth_chart_data))


def _playerid_positions(rows: bs4.ResultSet, *, css: str = "td", attr: str = "href") -> Generator[
    tuple[str, str], None, None
]:
    """

    :param rows:
    :param css:
    :param attr:
    :return:
    """
    for row in rows:
        try:
            yield re.search(
                r"playerid=(.*)&position=(.*)",
                row.select_one(css).select_one("a").attrs.get(attr)
            ).groups()
        except AttributeError:
            yield "", ""


def _playerid(rows: bs4.ResultSet, *, css: str = "td", attr: str = "href") -> Generator[
    str, None, None
]:
    """

    :param rows:
    :param css:
    :param attr:
    :return:
    """
    for row in rows:
        try:
            yield re.search(
                r"playerid=(.*)",
                row.select_one(css).select_one("a").attrs.get(attr)
            ).group(1)
        except AttributeError:
            yield ""


class Summary(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers"

    filename = "summary.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    class Data(NamedTuple):
        """

        """
        standings: pd.DataFrame
        depth_chart: _TeamDepthChart
        batting: pd.DataFrame
        pitching: pd.DataFrame

    def __stat_table(self, table_name: str) -> pd.DataFrame:
        """

        :param table_name:
        :return:
        """
        table = _stat_table(self.soup, table_name)
        table_data = self.scrape_table(
            table, css_r="tbody > tr,tfoot > tr.team-total"
        )
        dataframe = table_data.dataframe
        dataframe = dataframe.join(
            pd.DataFrame(
                _playerid_positions(table_data.row_elems),
                columns=["PlayerID", "Position"]
            )
        )
        breakpoint()
        dataframe = dataframe.apply(np.roll, shift=1)

        return dataframe

    def _standings(self) -> pd.DataFrame:
        """

        :return:
        """
        table = self.soup.select_one("table.team-standings")
        dataframe = self.scrape_table(
            table, css_h="tbody > tr:first-child", css_r="tbody > tr.team-row"
        ).dataframe

        dataframe.rename(
            columns={dataframe.columns[0]: "Team"},
            index=lambda i: i + 1,
            inplace=True
        )

        return dataframe

    def _depth_chart(self) -> _TeamDepthChart:
        """

        :return:
        """
        return _scrape_depth_chart(self.soup)

    def _batting(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Batting Stats Leaders")

    def _pitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Pitching Stats Leaders")

    def __data(self) -> Data:
        """

        :return:
        """
        return self.Data(
            self._standings(), self._depth_chart(), self._batting(), self._pitching()
        )

    def data(self, page) -> Data:
        return self.__data()

    async def adata(self, page) -> Data:
        return self.__data()


class Stats(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/stats"

    filename = "stats.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    class Data(NamedTuple):
        """

        """
        batting: pd.DataFrame
        spitching: pd.DataFrame
        rpitching: pd.DataFrame
        fielding: pd.DataFrame

    def __stat_table(self, table_name: str) -> pd.DataFrame:
        """

        :param table_name:
        :return:
        """
        table = _stat_table(self.soup, table_name)
        table_data = self.scrape_table(
            table, css_r="tbody > tr,tfoot > tr.team-total"
        )
        dataframe = table_data.dataframe
        dataframe = dataframe.join(
            pd.DataFrame(
                _playerid_positions(table_data.row_elems),
                columns=["PlayerID", "Position"]
            )
        )
        dataframe = dataframe.apply(np.roll, shift=1)

        return dataframe

    def _batting(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Batting Stats Leaders")

    def _spitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Starting Pitching Stats Leaders")

    def _rpitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Relief Pitching Stats Leaders")

    def _fielding(self) -> pd.DataFrame:
        """

        :return:
        """
        return self.__stat_table("Fielding Stats Leaders")

    def __data(self) -> Data:
        """

        :return:
        """
        return self.Data(
            self._batting(), self._spitching(), self._rpitching(), self._fielding()
        )

    def data(self, page) -> Data:
        return self.__data()

    async def adata(self, page) -> Data:
        return self.__data()


class Schedule(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/schedule"

    filename = "schedule.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    @staticmethod
    def __revise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        index = [
            df.columns[3], df.columns[5], df.columns[6]
        ]
        df[index] = df[index].replace("", np.NaN)
        return df

    def __data(self) -> pd.DataFrame:
        """

        :return:
        """
        table = self.soup.select_one("div.team-schedule-table > table")
        table_data = self.scrape_table(
            table, css_h="tr:first-child", css_r="tr:not(tr:first-child)"
        )

        dataframe = table_data.dataframe
        dataframe.rename(
            columns={
                dataframe.columns[1]: "vs/at",
                dataframe.columns[3]: re.sub(
                    r"^([A-Z]{3})Win Prob$", r"\1 Win Prob", dataframe.columns[3]
                ),
                dataframe.columns[5]: re.sub(
                    r"^([A-Z]{3})Runs$", r"\1 Runs", dataframe.columns[5]
                ),
                dataframe.columns[6]: "Opp Runs"
            },
            index=lambda i: i + 1,
            inplace=True
        )
        columns = [dataframe.columns[3], dataframe.columns[5], dataframe.columns[6]]
        dataframe[columns] = dataframe[columns].replace("", np.NaN)
        dataframe["Date"] = [
            datetime.datetime.strptime(
                r.select_one("td span.date-full").text, "%b %d, %Y"
            ) for r in table_data.row_elems
        ]
        dataframe = dataframe.join(
            pd.DataFrame(
                {
                    f"{dataframe.columns[-2]} PlayerID": _playerid(
                        table_data.row_elems, css="td.hi:nth-last-child(2)"
                    ),
                    f"{dataframe.columns[-1]} PlayerID": _playerid(
                        table_data.row_elems, css="td.hi:nth-last-child(1)"
                    )
                },
                index=dataframe.index
            )
        )

        return dataframe

    def data(self, page) -> pd.DataFrame:
        return self.__data()

    async def adata(self, page) -> pd.DataFrame:
        return self.__data()


class PlayerUsage(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/player-usage"

    filename = "player_usage.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    def __data(self) -> pd.DataFrame:
        """

        :return:
        """
        table = self.soup.select_one(".table-scroll")
        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe.rename(
            columns={
                **dict(zip(dataframe.columns[2:11], range(1, 10))),
                "Opp SP": "OppSP"
            },
            index=lambda i: i + 1,
            inplace=True
        )
        dataframe["Game Date"] = [
            datetime.datetime.strptime(
                r.select_one("td a").text, "%m/%d/%Y"
            ) for r in table_data.row_elems
        ]

        dataframe["OppSP Hand"] = [
            re.search(r"\(([LR])\) (.*)", x).group(1)
            for x in dataframe["OppSP"]
        ]
        dataframe["OppSP PlayerID"] = list(
            _playerid(table_data.row_elems, css="td[data-stat='Opp SP']")
        )
        dataframe["OppSP"] = dataframe["OppSP"].apply(
            lambda x: re.search(r"\(([LR])\) (.*)", x).group(2)
        )
        dataframe = dataframe.reindex(
            columns=[
                dataframe.columns[0], *dataframe.columns[2:-2],
                dataframe.columns[1], *dataframe.columns[-2:]
            ]
        )

        playerids_df = pd.DataFrame(
            columns=[f"{i} PlayerID" for i in range(1, 10)],
            index=dataframe.index
        )
        for i_ind, row in enumerate(table_data.row_elems):
            for i_col, elem in enumerate(row.select("td")[2:]):
                playerids_df.iloc[i_ind, i_col] = int(
                    re.search(
                        r"playerid=(.*)",
                        elem.select_one("a").attrs.get("href")
                    ).group(1)
                )
        for i_col, column in enumerate(playerids_df.columns, 1):
            dataframe.insert(
                loc=list(dataframe.columns).index(i_col) + 1,
                column=column,
                value=playerids_df.loc[:, column]
            )

        return dataframe

    def data(self, page) -> pd.DataFrame:
        return self.__data()

    async def adata(self, page) -> pd.DataFrame:
        return self.__data()


class DepthChart(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/depth-chart"

    filename = "depth_chart.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""

    class Data(NamedTuple):
        """

        """
        depth_chart: _TeamDepthChart
        batting: _BattingDepthChart
        pitching: _PitchingDepthChart

    def __dchart_tables(self, css: str) -> Generator[tuple[str, pd.DataFrame], None, None]:
        """

        :param css:
        :return:
        """
        for pos_elem in self.soup.select(css):
            table = pos_elem.select_one("div.team-stats-table > div.outer > div.inner > table")
            tname = "p_{}".format(
                pos_elem.select_one("div.team-depth-table-pos.team-color-primary").text
            )

            table_data = self.scrape_table(
                table, css_h="tbody > tr:first-child", css_r="tbody > tr:not(tr:first-child)"
            )

            dataframe = table_data.dataframe
            dataframe["PlayerID"] = list(_playerid(table_data.row_elems, css="td.frozen"))
            dataframe = dataframe.apply(np.roll, shift=1)

            yield tname, dataframe

    def _depth_chart(self) -> _TeamDepthChart:
        """

        :return:
        """
        return _scrape_depth_chart(self.soup)

    def _batting(self) -> _BattingDepthChart:
        """

        :return:
        """
        return _BattingDepthChart(**dict(self.__dchart_tables(".team-depth-table-bat")))

    def _pitching(self) -> _PitchingDepthChart:
        """

        :return:
        """
        return _PitchingDepthChart(**dict(self.__dchart_tables(".team-depth-table-pit")))

    def __data(self) -> Data:
        """

        :return:
        """
        return self.Data(
            self._depth_chart(), self._batting(), self._pitching()
        )

    def data(self, page) -> Data:
        """

        :param page:
        :return:
        """
        return self.__data()

    async def adata(self, page) -> Data:
        """

        :param page:
        :return:
        """
        return self.__data()
