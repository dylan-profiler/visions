Visions creates an internal type system representing the type of a pandas series rather than the underlying types of it's constituent objects. This allows us to flexibly perform sets of well defined operations over things like `Option[integer]` which might otherwise be upcast by pandas into `float`. This also allows us to produce more interesting summaries for data  which might otherwise simply be represented in pandas as `object`.

# Understanding Visions Types
Let's take the example of a timestamp:

```python
from visions.core.model_implementations import visions_timestamp

test_series = pd.Series([pd.datetime(2010, 1, 1), pd.datetime(2010, 8, 2), pd.datetime(2011, 2, 1), np.nan])
```

### Inference
Inference returns the narrowest possible type

```python
>>> get_type(test_series)
visions_datetime + missing
```

### Membership
We can do a couple of things with this, first we can check if `test_series` is a `visions_timestamp`

```python
>>> test_series in visions_datetime + missing
True

>>> test_series in visions_datetime
-> False
```


### Summarize
We can also get a summary unique to the visions_type of the data

```python
summarize(test_series, visions_datetime + missing)
-> {
	 'nunique': 3,
 	 'min': Timestamp('2010-01-01 00:00:00'),
 	 'max': Timestamp('2011-02-01 00:00:00'),
	 'n_records': 4,
	 'perc_unique': 1.0,
	 'range': Timedelta('396 days 00:00:00'),
	 'na_count': 1,
	 'perc_na': 0.25
   }
```

If we had instead applied a summarization operation to a categorical series we would get

```python
test_series = pd.Series(pd.Categorical([True, False, np.nan, 'test'], categories=[True, False, 'test', 'missing']))
summarize(test_series, visions_categorical)
-> {
    'nunique': 3,
    'n_records': 4,
    'category_size': 4,
    'missing_categorical_values': True,
    'na_count': 1,
    'perc_na': 0.25,
   }
```

Because Visions types are `Option[type]` by default, they all inherit the same missing value summaries (`na_count`, and `perc_na`), however, new visions types can be created at will if you prefer to produce your own summaries or extend your analysis to other types of objects.

By default Visions includes implementations for the following types:

* visions_integer
* visions_float
* visions_bool
* visions_categorical
* visions_complex
* visions_timestamp
* visions_object
* visions_string
* visions_geometry (these are shapely geometries)
