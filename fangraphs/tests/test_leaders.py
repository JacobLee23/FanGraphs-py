#! usr/bin/env python
# fangraphs/tests/test_leaders.py

"""

"""

import inspect

import pytest

from . import BaseTests
from . import get_soup
from .. import leaders


CLASSES = tuple(
    cls for name, cls in inspect.getmembers(leaders, inspect.isclass) if name != "FanGraphsPage"
)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_address(cls) -> None:
    """

    :param cls:
    """
    BaseTests._test_address(cls.address)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_path(cls) -> None:
    """

    :param cls:
    """
    BaseTests._test_path(cls.path)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_file_contents(cls) -> None:
    """

    :param cls:
    """
    BaseTests._test_file_contents(cls.path)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_filter_queries(cls) -> None:
    """

    :param cls:
    """
    soup = get_soup(cls.address)

    for qtypedict in cls.filter_queries.values():
        for querydict in qtypedict.values():
            for css in querydict.values():
                if isinstance(css, str):
                    BaseTests._test_selector(soup, css)
                else:
                    BaseTests._test_selectors(soup, css)
