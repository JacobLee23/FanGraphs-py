#! usr/bin/env python
# fangraphs/tests/test_teams.py

"""

"""

import pytest

from . import BaseTests
from .. import teams


CLASSES = (
    teams.Summary,
    teams.Stats,
    teams.Schedule,
    teams.PlayerUsage,
    teams.DepthChart
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
