#! usr/bin/env python
# fangraphs/tests/test_leaders.py

"""

"""

import pytest

from . import Runner
from .. import leaders


@pytest.mark.parametrize(
    "fgpage", (
        leaders.GameSpan,
        leaders.International,
        leaders.MajorLeague,
        leaders.SeasonStat,
        leaders.Splits,
        leaders.WAR
    )
)
def test_scraper(fgpage) -> None:
    """

    :param fgpage:
    """
    test_runner = Runner(fgpage)
    test_runner.test_address()
    test_runner.test_path()
    test_runner.test_file_contents()
