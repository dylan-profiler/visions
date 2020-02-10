Data Discovery and Data Integration
===================================

Data discovery is the task of finding data sets relevant to their task at hand.
Data integration is the task of combining those data sets.
*"No data scientist we have talked to reports spending less than 80% of his time on discovery and integration."* Stonebraker et al. report [stonebraker2018dataintegration]_.

The semantic types of data sets are critical for both tasks.

Data discovery can be supported by information retrieval systems.
Some queries like *"find a file with the extension CSV that contains 'url'"* and *"find a dataset that is under a public license matching 'titanic'"* are possible within current solutions based on full-text search and metadata standards [#f1]_, [#f2]_, [#f3]_.
However, queries based on the semantics of the data sets are out of reach of such approaches.
Semantic types could support systems, such as the knowledge-graph-based [aurum2018datadiscovery]_, to allow for queries as "find tables that contain a column with name 'ID' and have at least one column that looks like an input column".

Providing types and their relations can provide additional support for common operations in data integration.
Consider integrating two data sets, one coming from the office in New York, another from the same company but the one Amsterdam office.
Without proper typing, the "wages" column in the first data set might be in dollar, while the second one in euro.


.. [stonebraker2018dataintegration] Stonebraker, M., & Ilyas, I. F. (2018). Data Integration: The Current Status and the Way Forward. IEEE Data Eng. Bull., 41(2), 3-9.
.. [aurum2018datadiscovery] Fernandez, R. C., Abedjan, Z., Koko, F., Yuan, G., Madden, S., & Stonebraker, M. (2018, April). Aurum: A data discovery system. In 2018 IEEE 34th International Conference on Data Engineering (ICDE) (pp. 1001-1012). IEEE.

.. rubric:: Footnotes

.. [#f1] https://schema.org/Dataset
.. [#f2] https://developers.google.com/search/docs/data-types/dataset
.. [#f3] https://datasetsearch.research.google.com/
