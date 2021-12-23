#! usr/bin/env python
# fangraphs/tests/__init__.py

"""

"""

import json
import os
from urllib.request import urlopen

from ..data import data_file_path


QTYPES = (
    "selections", "dropdowns", "checkboxes", "switches"
)


class BaseTests:
    """
    
    """
    @staticmethod
    def test_address(address: str) -> None:
        """

        :param address:
        """
        with urlopen(address) as res:
            assert res.code == 200

    @staticmethod
    def test_filename(filename: str) -> None:
        """

        :param filename:
        """
        assert len(paths := [
            os.path.join(r, file)
            for r, d, f in os.walk(os.path.join("fangraphs", "data"))
            for file in f
            if file == filename
        ]) == 1, paths

    @staticmethod
    def test_file_contents(filename: str) -> None:
        """

        :param filename:
        """
        with open(data_file_path(filename), "r", encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, dict)
        assert all(k in QTYPES for k in data)
        assert all(
            isinstance(v, dict) for v in data.values()
        )
        assert all(
            isinstance(v, dict)
            for k in data for v in data[k].values()
        )
        assert all(
            isinstance(v, (str, list))
            for k in data for k_ in data[k] for v in data[k][k_].values()
        )
        assert all(
            isinstance(e, str)
            for k in data for k_ in data[k] for v in data[k][k_] for e in v
            if isinstance(v, list)
        )
