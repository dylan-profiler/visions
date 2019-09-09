#!/usr/bin/env python
# coding: utf-8

from tenzing.core.model_implementations.typesets import tenzing_complete_set
# from tenzing.core.typesets import infer_type
# from tenzing.core.model_implementations import *
import pandas as pd
import numpy as np
import networkx as nx
import datetime
import matplotlib.pyplot as plt


# In[3]:


df = pd.DataFrame({'item_id': [1, 1, 3], 
                   'item_cost': [2.1, 3.5, 4], 
                   'item_name': ['orange', 'orange', 'apple'],
                   'sale_date': pd.to_datetime([datetime.date(2011,1,1), datetime.date(2012, 1, 1), datetime.date(2013,1,1)]),
                   'store_location': pd.Series(['POINT (12 42)', 'POINT (100 42.723)', 'POINT (0 0)']),
                   'COGS': pd.Series([np.nan, 1.1, 2.1]).astype(str),
                   'is_still_available': [True, False, True],
                   'is_expired': ['True', 'false', 'False'],
                   'complex_record': [np.complex(1, 2), np.complex(3,4), np.complex(5, 6)]
                   })
print(df.dtypes)


# In[4]:


ts = tenzing_complete_set()
_ = ts.prep(df)

print(ts.summary_report(df))


# In[4]:


print(ts.column_type_map)


# In[5]:


print(ts.infer_types(df))


# In[6]:


print(ts.cast_to_inferred_types(df).dtypes)


# In[7]:


nx.draw_kamada_kawai(ts.relation_map, with_labels=True)

plt.show()
