from typing import Sequence

import numpy as np
import pandas as pd
import pandas.api.types as pdt

import visions
from visions.relations import IdentityRelation, TypeRelation
from visions.typesets.typeset import get_type_from_path


class Nominal(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Categorical)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return not pdt.is_categorical_dtype(series) or (
            pdt.is_categorical_dtype(series) and not series.cat.ordered
        )


class Categorical(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        # This example could be extended to show how low-cardinality discrete variables would be
        # inferred to nominal / ordinal. This can be achieved with an InferenceRelation.
        return [IdentityRelation(visions.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_object_dtype(series)


class Binary(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Nominal)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        state["n_distinct"] = state.get("n_distinct") or series.nunique()
        return state["n_distinct"] == 2


class Ordinal(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Categorical)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered


class Numeric(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(visions.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_numeric_dtype(series)


class Continuous(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Numeric)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return not pdt.is_integer_dtype(series)


class Discrete(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Numeric)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_integer_dtype(series)


class VariableTypeset(visions.VisionsTypeset):
    def __init__(self):
        types = {
            visions.Generic,
            Categorical,
            Nominal,
            Ordinal,
            Numeric,
            Continuous,
            Discrete,
            Binary,
        }
        super().__init__(types)


variable_set = VariableTypeset()
variable_set.output_graph("variable_set.pdf")


class Classification(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(visions.Generic)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        return state["dtype"] in [Nominal, Categorical, Ordinal, Binary]


class BinaryClassification(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        return state["dtype"] == Binary


class MultiClassification(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        return state["dtype"] != Binary


class Regression(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(visions.Generic)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        return state["dtype"] in [Continuous, Discrete]


class PoissonRegression(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Regression)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        if not state["dtype"] == Discrete:
            return False

        # This is a simplified test if poisson regression applies that doesn't take into account if
        # the ratio is significant
        state["mean_var_ratio"] = state.get("mean_var_rate") or np.mean(
            series
        ) / np.var(series)
        return np.isclose(state["mean_var_ratio"], 1, rtol=0.05)


class NegBinomRegression(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Regression)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        if not state["dtype"] == Discrete:
            return False

        # See comment at poisson regression
        state["mean_var_ratio"] = state.get("mean_var_rate") or np.mean(
            series
        ) / np.var(series)
        return state["mean_var_ratio"] > 1.05


class OrdinalRegression(visions.VisionsBaseType):
    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        return [IdentityRelation(Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state["dtype"] = state.get("dtype") or variable_set.detect_type(series)
        return state["dtype"] == Ordinal


class MLProblemTypeset(visions.VisionsTypeset):
    def __init__(self):
        types = {
            visions.Generic,
            Classification,
            BinaryClassification,
            MultiClassification,
            Regression,
            NegBinomRegression,
            PoissonRegression,
            OrdinalRegression,
        }
        super().__init__(types)


problem_set = MLProblemTypeset()
problem_set.output_graph("problem_set.pdf")


# Example
dataset = pd.DataFrame(
    {
        "target_3": ["cat", "dog", "dog", "cat", "horse"],
        "target_2": ["cat", "dog", "dog", "cat", "dog"],
        "target_num": [1, 2, 2, 1, 2],
    }
)


for target in dataset.columns:
    _, problem_types, state = problem_set.detect(dataset[target])
    problem_type = get_type_from_path(problem_types)

    print(
        f"The target variable '{target}' is of the {state['dtype']} statistical type."
    )
    print(f"Our logic found that a {problem_type} model should be used.")
