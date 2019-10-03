from urllib.parse import urlparse

import numpy as np


a = np.array([["http", "www.google.com", "/blaat", "", "", ""] * 100])
print(a)
print(a.nbytes)

b = np.array(["http://www.google.com/blaat"] * 100)
print(b)
print(b.nbytes)
