from typing import Sequence
import pandas as pd
import pandas.api.types as pdt
import numpy as np
import visions
from visions.relations import TypeRelation, IdentityRelation
from visions.typesets.typeset import get_type_from_path


class Nominal(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Categorical)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return not pdt.is_categorical_dtype(series) or (pdt.is_categorical_dtype(series) and not series.cat.ordered)


class Categorical(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        # This example could be extended to show how low-cardinality discrete variables would be
        # inferred to nominal / ordinal. This can be achieved with an InferenceRelation.
        return [IdentityRelation(cls, visions.Generic)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return pdt.is_object_dtype(series)


class Binary(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Nominal)]

    @classmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        state['n_distinct'] = state.get('n_distinct') or series.nunique()
        return state['n_distinct'] == 2


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
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, visions.Generic)]

    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        return state['dtype'] in [Nominal, Categorical, Ordinal, Binary]


class BinaryClassification(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        return state['dtype'] == Binary


class MultiClassification(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Classification)]

    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        return state['dtype'] != Binary


class Regression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        return state['dtype'] in [Continuous, Discrete]

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, visions.Generic)]


class PoissonRegression(visions.VisionsBaseType):
    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Regression)]

    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        if not state['dtype'] == Discrete:
            return False

        # This is a simplified test if poisson regression applies that doesn't take into account if
        # the ratio is significant
        state['mean_var_ratio'] = state.get('mean_var_rate') or np.mean(series) / np.var(series)
        return np.isclose(state['mean_var_ratio'], 1, rtol=0.05)


class NegBinomRegression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        if not state['dtype'] == Discrete:
            return False

        # See comment at poisson regression
        state['mean_var_ratio'] = state.get('mean_var_rate') or np.mean(series) / np.var(series)
        return state['mean_var_ratio'] > 1.05

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Regression)]


class OrdinalRegression(visions.VisionsBaseType):
    @classmethod
    def contains_op(cls, series, state):
        state['dtype'] = state.get('dtype') or variable_set.detect_type(series)
        return state['dtype'] == Ordinal

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return [IdentityRelation(cls, Classification)]


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
            OrdinalRegression
        }
        super().__init__(types)


problem_set = MLProblemTypeset()
problem_set.output_graph("problem_set.pdf")


# Example
dataset = pd.DataFrame({
    "target_3": ["cat", "dog", "dog", "cat", "horse"],
    "target_2": ["cat", "dog", "dog", "cat", "dog"],
    "target_num": [1, 2, 2, 1, 2],
})


for target in dataset.columns:
    _, problem_types, state = problem_set.detect(dataset[target])
    problem_type = get_type_from_path(problem_types)

    print(
        f"The target variable '{target}' is of the {state['dtype']} statistical type."
    )
    print(
        f"Our logic found that a {problem_type} model should be used."
    )
