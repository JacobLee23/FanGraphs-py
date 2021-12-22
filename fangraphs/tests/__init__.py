#! usr/bin/env python
# fangraphs/tests/__init__.py

"""

"""

import json
import os
from urllib.request import urlopen


QTYPES = (
    "selections", "dropdowns", "checkboxes", "switches"
)


class Runner:
    """
    
    """
    def __init__(self, fgpage):
        """
        :param fgpage:
        """
        self.fgpage = fgpage

    def test_address(self) -> None:
        """
        
        """
        with urlopen(self.fgpage.address) as res:
            assert res.code == 200
            
    def test_path(self) -> None:
        """
        
        """
        assert os.path.exists(self.fgpage.path)

    def test_file_contents(self) -> None:
        """

        """
        with open(self.fgpage.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        assert data

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
