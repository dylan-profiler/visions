# Tangled up in Unicode

This module provides an alternative to Python's `unicodedata`, including human-readable property representations.

## Properties

| Property				| `tangledUpInUnicode`			| `unicodedata` 		|
|-----------------------|-------------------------------|-----------------------|
| Name					| &#9745;						| &#9745;  				|
| Decimal				| &#9745;						| &#9745;  				|
| Digit					| &#9745;						| &#9745;  				|
| Numeric				| &#9745;						| &#9745;  				|
| Combining           	| &#9745;						| &#9745;  				|
| Mirrored           	| &#9745;						| &#9745;  				|
| Decomposition        	| &#9745;						| &#9745;  				|
| Category				| &#9745; + alias				| &#9745;  				|
| Bidirectional			| &#9745; + alias				| &#9745;  				|
| East Asian Width		| &#9745; + alias				| &#9745;  				|
| Script				| &#9745;						| -  					|
| Block					| &#9745;						| -  					|
| PropList				| &#9745;						| -  					|

_Table 1: presence of properties is denoted by &#9745; (Unicode Character 'BALLOT BOX WITH CHECK' (U+2611))._		

## Usage

```python
import tangled_up_in_unicode as unicodedata
```

The package can be installed from pypi:

```
pip install tangled-up-in-unicode
```

## Other features

Some of the features in `unicodedata` are not supported. 

| Feature				| `tangledUpInUnicode`			| `unicodedata` 		|
|-----------------------|-------------------------------|-----------------------|
| lookup	           	| -								| &#9745;  				|
| normalize           	| -								| &#9745;  				|
| unidata_version      	| -								| &#9745;  				|
| ucd_3_2_0      		| -								| &#9745;  				|

