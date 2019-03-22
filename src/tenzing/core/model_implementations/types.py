from tenzing.core.models import tenzing_model, model_relation, optionMixin, relationMixin
from tenzing.utils import singleton
import pandas.api.types as pdt


@singleton.singleton_object
class tenzing_integer(optionMixin, relationMixin, tenzing_model):
    def contains_op(self, series):
        if pdt.is_integer_dtype(series):
            return True
        else:
            # Need this additional check because it's an Option[Int] which in
            # pandas land will result in integers with decimal trailing 0's
            return series.eq(series.astype(int))

    def cast_op(self, series):
        return series.as_type(int)


@singleton.singleton_object
class tenzing_float(optionMixin, relationMixin, tenzing_model):
    def contains_op(self, series):
        return pdt.is_float_dtype(series)

    def cast_op(self, series):
        return series.as_type('float')


def register_integer_relations():
    int_float_relation = model_relation(tenzing_float, lambda x: False, lambda x: False)
    tenzing_integer.register_relation(int_float_relation)


register_integer_relations()
