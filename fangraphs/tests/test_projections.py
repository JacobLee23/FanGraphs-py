#! usr/bin/env python
# fangraphs/tests/test_projections.py

"""

"""

import pytest

from . import BaseTests
from .. import projections


@pytest.mark.parametrize(
    "fgpage", (
        projections.Projections,
    )
)
def test_address(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_address(fgpage.address)


@pytest.mark.parametrize(
    "fgpage", (
        projections.Projections,
    )
)
def test_filename(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_filename(fgpage.filename)


@pytest.mark.parametrize(
    "fgpage", (
        projections.Projections,
    )
)
def test_file_contents(fgpage) -> None:
    """

    :param fgpage:
    """
    BaseTests.test_file_contents(fgpage.filename)
