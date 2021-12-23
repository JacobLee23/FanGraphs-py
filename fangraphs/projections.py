#! usr/bin/env python
# fangraphs/projections.py

"""

"""

import pandas as pd

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


class Projections(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/projections.aspx"

    filename = "projections.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = "#ProjectionBoard1_cmdCSV"

    def data(self, page) -> pd.DataFrame:
        dataframe = self.export_data(page)

        dataframe.drop(columns=["-1", "-1.1", "-1.2", "-1.3"], inplace=True)

        return dataframe

    async def adata(self, page) -> pd.DataFrame:
        dataframe = await self.aexport_data(page)

        dataframe.drop(columns=["-1", "-1.1", "-1.2", "-1.3"], inplace=True)

        return dataframe
