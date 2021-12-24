#! usr/bin/env python
# fangraphs/teams.py

"""

"""

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


class Summary(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers"

    filename = "summary.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class Stats(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/stats"

    filename = "stats.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class Schedule(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/schedule"

    filename = "schedule.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class PlayerUsage(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/player-usage"

    filename = "player_usage.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""


class DepthChart(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/teams/dodgers/depth-chart"

    filename = "depth_chart.json"
    filter_queries = load_filter_queries(filename)

    export_data_css = ""
