import visions.backends.python

try:
    import pandas as pd

    import visions.backends.pandas
    from visions.backends.pandas.test_utils import pandas_version

    if pandas_version[0] < 1:
        from visions.dtypes.boolean import BoolDtype
except ImportError:
    pass


try:
    import numpy as np

    import visions.backends.numpy
except ImportError:
    pass


