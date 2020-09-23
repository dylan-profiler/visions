try:
    import pandas as pd

    import visions.backends.pandas_functions

    if int(pd.__version__.split(".")[0]) < 1:
        from visions.dtypes.boolean import BoolDtype
except ImportError:
    pass

try:
    import numpy as np
    import visions.backends.numpy_functions
except ImportError:
    pass
