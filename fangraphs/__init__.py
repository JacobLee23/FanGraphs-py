#! usr/bin/env python
# fangraphs/__init__.py

"""

"""

import re
from typing import NamedTuple

from .logger import logger
from .scraper import AsyncScraper
from .scraper import SyncScraper


class RegularExpression(NamedTuple):
    """

    """
    playerid: re.Pattern = re.compile(r"playerid=(.*)")
    position: re.Pattern = re.compile(r"position=(.*)")
    playerid_position: re.Pattern = re.compile(r"playerid=(.*)&position=(.*)")


RegEx = RegularExpression()
