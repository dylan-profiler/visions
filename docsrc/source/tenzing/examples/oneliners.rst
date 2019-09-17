One line examples
=================


Membership
----------
Membership: check whether a series is of type X. We should make design decisions on the exact behaviour.


Function signature:

`X in Partitioner -> bool`

==================================================== ==========================
Code										         Result
---------------------------------------------------- --------------------------
`Series([T, F]) in type[type_bool]`			         True
`Series([T, F]) in type[type_generic]`			     True
`Series([T, F]) in type[type_integer]`			     False
`Series([T, F, nan]) in type[type_bool]`		     False
`Series([T, F, nan]) in missing | type[type_bool]`	 True
`Series([T, F]) in missing | type[type_bool]`		 True
`Series([T, F]) in type_bool`				         Exception
`Series([T, F, np.nan]) in type_bool`                missing
`Series([np.nan]) in missing_generic`			     Exception
`Series([np.nan]) in missing`				         True
`Series([np.nan]) in missing[missing_generic]`	     True (equivalent to above)
==================================================== ==========================

Get Type
--------

Inference: determine the current type of a series S. We choose the most specific one, without conversion (casting and coercion).
Start at the root RootPartitioner.
For each partitioner with a non-empty mask, traverse the graph (DFS) and return the base_type
Return the Multipartitioner with individual partitioners and their inferred type.
If the inferred type is *_generic, default to the partitioner name alone (e.g. type[type_generic] -> type).

Function signature:
`typeset.get_type(S, convert=False) -> Partitioner`


`typeset.get_type(Series([T, F])`			-> type[type_bool]
`typeset.get_type(Series([np.nan])`			-> missing
`typeset.get_type(Series([T, F, np.nan])`		-> type[type_bool] | missing
`typeset.get_type(Series([“test”, “NAN”])`		-> type[type_string]
`typeset.get_type(Series([“http://bobdylan.com”])`	-> type[type_string]
`typeset.get_type(Series([1.0, 2.0, 3.0])`		-> type[type_integer]
`typeset.get_type(Series([])`				-> ? (open for discussion)
`typeset.get_type(Series([1.0, np.nan])`		-> type[type_integer] | missing
`typeset.get_type(Series([1, 2, 3, np.inf])`		-> type[type_integer] | infinite


Conversion
----------

Conversion: Converts the Series based on the relations specified on the types in the typeset. Obviously, the series and its type should be untouched if no conversion has taken place.


Related methods: `typeset.get_type(S, convert=True) -> Partitioner`
Examples 	typeset.convert_series(S) -> S
`typeset.convert_series(Series([T, F])`			-> Series([T, F])
type[type_bool] 						-> type[type_bool])

`typeset.convert_series(Series([“T”, “F”])`			-> Series([T, F])
Type[type_string]						-> type[type_bool]

`typeset.convert_series(Series([“NAN”])`			-> Series([np.nan])
type[type_string] 						-> missing

`typeset.convert_series(Series([“http://bobdylan.com”])`	-> Series([url(...)])
type[type_string]						-> type[type_url]

`typeset.convert_series(Series([None, None])`		-> Series([None, None])
type[type_object]						-> type[type_object]

`typeset.convert_series(Series([func1, func2])`		-> Series([func1, func2])
type[type_object]						-> type[type_object]

