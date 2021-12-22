#! usr/bin/env python
# fangraphs/tests/test_leaders.py

"""

"""

import pytest

from . import BaseTests
from . import get_classes
from .. import leaders


CLASSES = get_classes(leaders)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_address(cls) -> None:
    """

    :param cls:
    """
    BaseTests.test_address(cls.address)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_path(cls) -> None:
    """

    :param cls:
    """
    BaseTests.test_path(cls.path)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_file_contents(cls) -> None:
    """

    :param cls:
    """
    BaseTests.test_file_contents(cls.path)


@pytest.mark.parametrize(
    "cls", CLASSES
)
def test_filter_queries(cls) -> None:
    """

    :param cls:
    """
    soup = BaseTests.get_soup(cls.address)

    for qtypedict in cls.filter_queries.values():
        for querydict in qtypedict.values():
            for css in querydict.values():
                if isinstance(css, str):
                    BaseTests.test_selector(soup, css)
                else:
                    BaseTests.test_selectors(soup, css)
