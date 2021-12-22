#! usr/bin/env python
# fangraphs/tests/test_leaders.py

"""

"""

import inspect

import pytest

from . import _test_address
from . import _test_file_contents
from . import _test_path
from .. import leaders


classes = tuple(
    cls for name, cls in inspect.getmembers(leaders, inspect.isclass) if name != "FanGraphsPage"
)


@pytest.mark.parametrize(
    "cls", classes
)
def test_address(cls) -> None:
    """

    :param cls:
    """
    _test_address(cls.address)


@pytest.mark.parametrize(
    "cls", classes
)
def test_path(cls) -> None:
    """

    :param cls:
    """
    _test_path(cls.path)


@pytest.mark.parametrize(
    "cls", classes
)
def test_file_contents(cls) -> None:
    """

    :param cls:
    """
    _test_file_contents(cls.path)
