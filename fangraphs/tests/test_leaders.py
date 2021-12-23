#! usr/bin/env python
# fangraphs/tests/test_leaders.py

"""

"""

import pytest

from . import BaseTests
from .. import leaders


CLASSES = (
    leaders.GameSpan,
    leaders.International,
    leaders.MajorLeague,
    leaders.SeasonStat,
    leaders.Splits,
    leaders.WAR
)


@pytest.mark.parametrize(
    "fgpage", CLASSES
)
def test_address(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_address(fgpage.address)


@pytest.mark.parametrize(
    "fgpage", CLASSES
)
def test_filename(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_filename(fgpage.filename)


@pytest.mark.parametrize(
    "fgpage", CLASSES
)
def test_file_contents(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_file_contents(fgpage.filename)
