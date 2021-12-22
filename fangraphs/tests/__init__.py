#! usr/bin/env python
# fangraphs/tests/__init__.py

"""

"""

import os
import json
from urllib.request import urlopen


QTYPES = (
    "selections", "dropdowns", "checkboxes", "switches"
)


def _test_address(address: str) -> None:
    """

    :param address:
    """
    assert urlopen(address).code == 200


def _test_path(path: str) -> None:
    """

    :param path:
    """
    assert os.path.exists(path)


def _test_file_contents(path: str) -> None:
    """

    :param path:
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data

    assert isinstance(data, dict)
    assert all(k in QTYPES for k in data)
    assert all(isinstance(v, dict) for v in data.values())
    assert all(isinstance(v, dict) for k in data for v in data[k].values())
    assert all(isinstance(v, (str, list)) for k in data for k_ in data[k] for v in data[k][k_].values())
    assert all(isinstance(e, str) for k in data for k_ in data[k] for v in data[k][k_] for e in v if isinstance(v, list))
