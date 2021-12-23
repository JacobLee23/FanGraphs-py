#! usr/bin/env python
# fangraphs/data/__init__.py

"""

"""

import os
from typing import Optional

from .. import logger


def data_file_path(filename: str) -> str:
    """

    :param filename:
    :return:
    """
    logger.debug("Searching for %s", filename)

    path = next(
        os.path.join(r, file)
        for r, d, f in os.walk(os.path.join("fangraphs", "data"))
        for file in f
        if file == filename
    )
    logger.debug("Found %s at %s", filename, path)

    return path
