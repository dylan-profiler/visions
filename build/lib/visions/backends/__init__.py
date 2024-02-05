import logging

logger = logging.getLogger(__name__)


try:
    import pandas as pd

    import visions.backends.pandas
    from visions.backends.pandas.test_utils import pandas_version

    if pandas_version[0] < 1:
        from visions.dtypes.boolean import BoolDtype
    logger.info(f"Pandas backend loaded {pd.__version__}")

except ImportError:
    logger.info("Pandas backend NOT loaded")


try:
    import numpy as np

    import visions.backends.numpy

    logger.info(f"Numpy backend loaded {np.__version__}")
except ImportError:
    logger.info("Numpy backend NOT loaded")


try:
    import pyspark

    import visions.backends.spark

    logger.info(f"Pyspark backend loaded {pyspark.__version__}")
except ImportError:
    logger.info("Pyspark backend NOT loaded")


try:
    import visions.backends.python

    logger.info("Python backend loaded")
except ImportError:
    logger.info("Python backend NOT loaded")
