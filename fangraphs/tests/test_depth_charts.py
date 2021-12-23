#! usr/bin/env python
# fangraphs/tests/test_depth_charts.py

"""

"""

import pytest

from . import BaseTests
from .. import depth_charts


@pytest.mark.parametrize(
    "fgpage", (
        depth_charts.Standings,
        depth_charts.BaseRuns,
        depth_charts.DepthCharts,
        depth_charts.PC,
        depth_charts.P1B,
        depth_charts.P2B,
        depth_charts.PSS,
        depth_charts.P3B,
        depth_charts.PLF,
        depth_charts.PCF,
        depth_charts.PRF,
        depth_charts.PSP,
        depth_charts.PRP,
        depth_charts.Totals
    )
)
def test_address(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_address(fgpage.address)


@pytest.mark.parametrize(
    "fgpage", (
        depth_charts.Standings,
        depth_charts.BaseRuns,
        depth_charts.DepthCharts,
        depth_charts.PC,
        depth_charts.P1B,
        depth_charts.P2B,
        depth_charts.PSS,
        depth_charts.P3B,
        depth_charts.PLF,
        depth_charts.PCF,
        depth_charts.PRF,
        depth_charts.PSP,
        depth_charts.PRP,
        depth_charts.Totals
    )
)
def test_filename(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_filename(fgpage.filename)


@pytest.mark.parametrize(
    "fgpage", (
        depth_charts.Standings,
        depth_charts.BaseRuns,
        depth_charts.DepthCharts,
        depth_charts.PC,
        depth_charts.P1B,
        depth_charts.P2B,
        depth_charts.PSS,
        depth_charts.P3B,
        depth_charts.PLF,
        depth_charts.PCF,
        depth_charts.PRF,
        depth_charts.PSP,
        depth_charts.PRP,
        depth_charts.Totals
    )
)
def test_file_contents(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_file_contents(fgpage.filename)

