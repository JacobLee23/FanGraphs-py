#! usr/bin/env python
# fangraphs/data/__init__.py

"""

"""

import os
from typing import Optional

from .. import logger


def data_file_path(filename: str) -> Optional[str]:
    """

    :param filename:
    :return:
    """
    logger.debug("Searching for %s", filename)

    for root, directories, files in os.walk(os.path.join("fangraphs", "data")):
        for file in files:
            if file == filename:
                path = os.path.join(root, file)
                logger.debug("Found %s at %s", filename, path)

                return path
