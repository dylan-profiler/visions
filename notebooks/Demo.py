#!/usr/bin/env python
# coding: utf-8
import json

from tenzing.core.model_implementations.typesets import tenzing_complete_set
# from tenzing.core.typesets import infer_type
# from tenzing.core.model_implementations import *
import pandas as pd
import numpy as np
import networkx as nx
import datetime
import matplotlib.pyplot as plt


df = pd.DataFrame({'item_id': [1, 1, 3],
                   'item_cost': [2.1, 3.5, 4],
                   'item_name': ['orange', 'orange', 'apple'],
                   'sale_date': pd.to_datetime([datetime.date(2011,1,1), datetime.date(2012, 1, 1), datetime.date(2013,1,1)]),
                   'store_location': pd.Series(['POINT (12 42)', 'POINT (100 42.723)', 'POINT (0 0)']),
                   # 'COGS': pd.Series([np.nan, 1.1, 2.1]).astype(str),
                   'is_still_available': [True, False, True],
                   'is_expired': ['True', 'false', 'False'],
                   'is_person': ['Y', 'N', 'Y'],
                   'website': ['http://www.google.com', 'http://www.bing.com', 'http://www.duckduckgo.com'],
                   'complex_record': [np.complex(1, 2), np.complex(3,4), np.complex(5, 6)]
                   })

# df = pd.read_csv('https://github.com/johnhagler/tb_viz/raw/4f1839e43e0d81b2f0dfdcac7e4d6b6cf3c4509e/incidence.csv')


ts = tenzing_complete_set()
_ = ts.prep(df)

summary = ts.summary_report(df)
# print(json.dumps(summary, indent=4))


# In[4]:


# print(ts.column_type_map)


# In[5]:


print(ts.infer_types(df))


# In[6]:


df_clean = ts.cast_to_inferred_types(df)
print(df_clean.head())

# TODO: assert
# {'item_id': tenzing_integer,
# 'item_cost': tenzing_float,
# 'item_name': tenzing_string,
# 'sale_date': tenzing_timestamp,
# 'store_location': tenzing_geometry,
# 'COGS': tenzing_float,
# 'is_still_available': tenzing_bool,
# 'is_expired': tenzing_bool,
# 'is_person': tenzing_bool,
# 'website': tenzing_url,
# 'complex_record': tenzing_complex}
print(ts.infer_types(df_clean))

ts.plot()

plt.show()
