Tenzing creates an internal type system representing the type of a pandas series rather than the underlying types of it's constituent objects. This allows us to flexibly perform sets of well defined operations over things like `Option[integer]` which might otherwise be upcast by pandas into `float`. This also allows us to produce more interesting summaries for data  which might otherwise simply be represented in pandas as `object`.

### Understanding Tenzing Types
Let's take the example of a timestamp:

```python
from tenzing.core.model_implementations import tenzing_timestamp

test_series = pd.Series([pd.datetime(2010, 1, 1), pd.datetime(2010, 8, 2), pd.datetime(2011, 2, 1), np.nan])
```

We can do a couple of things with this, first we can check if `test_series` is a `tenzing_timestamp`

```python
test_series in tenzing_timestamp
-> True
```

We can also get a summary unique to the tenzing_type of the data

```python
tenzing_timestamp.summarize(test_series)
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
tenzing_categorical.summarize(test_series)
-> {
    'nunique': 3,
    'n_records': 4,
    'category_size': 4,
    'missing_categorical_values': True,
    'na_count': 1,
    'perc_na': 0.25,
   }
```

Because Tenzing types are `Option[type]` by default, they all inherit the same missing value summaries (`na_count`, and `perc_na`), however, new tenzing types can be created at will if you prefer to produce your own summaries or extend your analysis to other types of objects.

By default Tenzing includes implementations for the following types:

* tenzing_integer
* tenzing_float
* tenzing_bool
* tenzing_categorical
* tenzing_complex
* tenzing_timestamp
* tenzing_object
* tenzing_string
* tenzing_geometry (these are shapely geometries)

### Tenzing Typesets

Types can also be organized into groups of types to perform analysis over a dataframe or collection of series. These are called tenzing typesets.

```python
from tenzing.core.model_implementations.typesets import tenzing_standard

df = pd.DataFrame({'a': range(3),
			         'b': [2 * i for i in range(3)],
			         'c': ['howdy', 'howdy', 'doody']})
my_typeset = tenzing_standard()
my_typeset.types
-> frozenset({tenzing_bool,
           tenzing_categorical,
           tenzing_complex,
           tenzing_float,
           tenzing_integer,
           tenzing_object,
           tenzing_string,
           tenzing_timestamp})
```

The standard typeset includes all of the baseline tenzing types except geometries. Each typeset is unique to a dataset for caching purposes and can apply the same methods, like `summarize`, as a tenzing type.

```python
my_typeset.prep(df)
my_typeset.summarize(df)
-> {'a': {'nunique': 3.0,
		   'mean': 1.0,
		   'std': 1.0,
		   'max': 2.0,
  		   'min': 0.0,
		   'median': 1.0,
		   'n_records': 3,
		   'n_zeros': 1,
		   'perc_zeros': 0.3333333333333333,
		   'na_count': 0,
		   'perc_na': 0.0
		  },
 'b': { 'nunique': 3.0,
		 'mean': 2.0,
		 'std': 2.0,
		 'max': 4.0,
		 'min': 0.0,
		 'median': 2.0,
		 'n_records': 3,
		 'n_zeros': 1,
		 'perc_zeros': 0.3333333333333333,
		 'na_count': 0,
		 'perc_na': 0.0
		},
 'c': { 'nunique': 2,
        'n_records': 3,
        'frequencies': {'howdy': 2, 'doody': 1},
        'na_count': 0,
        'perc_na': 0.0
       }
 }


```

## Custom Tenzing Types


Each Tenzing type is a singleton object extending the basic `tenzing_model` requiring a unique implementation of three methods:

1. `contains_op`. Checks whether a series is of the type tenzing_type, returns Bool.
2. `summarization_op`. Performs a set of summarization procedures unique to this tenzing type and returns their output as a dict.
3. `cast_op`. This is going away, needs to be folded into model_relations [TODO]


All tenzing_types can be made into `Option[tenzing_type]` by inheriting from `optionMixin` in `tenzing.core.Mixins`.

```python
from tenzing.core.models import tenzing_model
from tenzing.utils import singleton
from tenzing.core.mixins import optionMixin

@singleton.singleton_object
class tenzing_timestamp(optionMixin, tenzing_model):
    def contains_op(self, series):
        return pdt.is_datetime64_dtype(series)

    def cast_op(self, series):
        return pd.to_datetime(series)

    def summarization_op(self, series):
        aggregates = ['nunique', 'min', 'max']
        summary = series.agg(aggregates).to_dict()

        summary['n_records'] = series.shape[0]
        summary['perc_unique'] = summary['nunique'] / summary['n_records']

        summary['range'] = summary['max'] - summary['min']
        return summary
```
