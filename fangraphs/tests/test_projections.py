#! usr/bin/env python
# fangraphs/tests/test_projections.py

"""

"""

import pytest

from . import Runner
from .. import projections


@pytest.mark.parametrize(
    "fgpage", (
        projections.Projections
    )
)
def test_scraper(fgpage) -> None:
    """

    :param fgpage:
    """
    test_runner = Runner(fgpage)
    test_runner.test_address()
    test_runner.test_path()
    test_runner.test_file_contents()

