import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


try:
    import pandas as pd

    import visions.backends.pandas_be
    from visions.backends.pandas_be.test_utils import pandas_version

    if pandas_version[0] < 1:
        from visions.dtypes.boolean import BoolDtype
    logger.debug(f"Pandas backend loaded {pd.__version__}")

except ImportError:
    logger.debug("Pandas backend NOT loaded")


try:
    import numpy as np

    import visions.backends.numpy_

    logger.debug(f"Numpy backend loaded {np.__version__}")
except ImportError:
    logger.debug("Numpy backend NOT loaded")



import visions.backends.python_

logger.debug("Python backend loaded")
