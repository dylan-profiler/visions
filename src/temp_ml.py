from typing import Sequence
import pandas as pd
import pandas.api.types as pdt
import visions
from visions.relations import TypeRelation, IdentityRelation


class Nominal(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Categorical)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return not pdt.is_categorical_dtype(series) or (
            pdt.is_categorical_dtype(series) and not series.cat.ordered
        )


class Categorical(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, visions.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_object_dtype(series)


class Ordinal(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Categorical)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered


class Numeric(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, visions.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_numeric_dtype(series)


class Continuous(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Numeric)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return not pdt.is_integer_dtype(series)


class Discrete(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Numeric)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_integer_dtype(series)


class Classification(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Nominal)]

    @classmethod
    def contains_op(cls, series, state):
        return series in Nominal or series in Ordinal


class BinaryClassification(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state["n_distinct"] = state.get("n_distinct") or series.nunique()
        return state["n_distinct"] == 2


class MultiClassification(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state["n_distinct"] = state.get("n_distinct") or series.nunique()
        return state["n_distinct"] > 2


class Regression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        return series in Continuous or series in Discrete

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Continuous)]


class PoissonRegression2(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        if series not in Discrete:
            return False
        mean_var_ratio = np.mean(series) / np.var(series)
        return (mean_var_ratio > 0.95) and (mean_var_ratio < 1.05)

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Discrete)]


class NegBinomRegression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        if series not in Discrete:
            return False

        return np.var(series) > (1.05 * np.mean(series))

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Discrete)]


class OrdinalRegression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        return series in Ordinal

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Ordinal)]


class MLProblemTypeset(visions.VisionsTypeset):
    def __init__(self):
        types = {
            visions.Generic,
            Categorical,
            Nominal,
            Ordinal,
            Numeric,
            Continuous,
            Discrete,
            Classification,
            BinaryClassification,
            MultiClassification,
            Regression,
            NegBinomRegression,
            PoissonRegression,
            OrdinalRegression,
        }
        super().__init__(types)


import numpy as np
from visions import CompleteSet

variable_set = CompleteSet()


class PoissonRegression(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Regression)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        if not state["dtype"] == Discrete:
            return False
        mean_var_ratio = np.mean(series) / np.var(series)
        return np.isclose(mean_var_ratio, rtol=0.05)


typeset = MLProblemTypeset()

typeset.output_graph("problem_set.pdf")

dataset = pd.DataFrame({"target": ["cat", "dog", "dog", "cat", "horse"]})
target = "target"
problem_type, state = typeset.detect_type(dataset)
print(f"The target variable '{target}' is of the {state['var_type']} statistical type.")
print(f"Our logic found that a {problem_type} model should be used.")
