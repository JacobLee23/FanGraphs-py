#! usr/bin/env python
# fangraphs/scores.py

"""

"""

from .scraper import FanGraphsPage
from .scraper import load_filter_queries


class LiveScoreboard(FanGraphsPage):
    """

    """
    address = "https://www.fangraphs.com/livescoreboard.aspx"

    filename = "live_scoreboard.json"
    filter_queries = load_filter_queries(filename)


class LiveLeaderboards(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/scores/live-leaderboards"

    filename = "live_leaderboards.json"
    filter_queries = load_filter_queries(filename)


class Scoreboard(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/scoreboard.aspx"

    filename = "scoreboard.json"
    filter_queries = load_filter_queries(filename)


class GameGraphs(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/wins.aspx"

    filename = "game_graphs.json"
    filter_queries = load_filter_queries(filename)


class PlayLog(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/plays.aspx"

    filename = "play_log.json"
    filter_queries = load_filter_queries(filename)


class BoxScore(FanGraphsPage):
    """

    """
    address = "https://fangraphs.com/boxscore.aspx"

    filename = "box_score.json"
    filter_queries = load_filter_queries(filename)
