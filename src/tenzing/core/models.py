from abc import abstractmethod
import pandas as pd


class model_relation:
    """Relationship encoder between implementations of :class:`tenzing.core.models.tenzing_model`

    Defines a one to one relationship between two tenzing_model implementations,
    A and B, with respect to an underlying data series. In order to define a relationship we need
    two methods:

        - **is_relationship**, determines whether a series of type B can be alternatively represented as type A.
        - **transform**, provides a mechanism to convert the series from B -> A.

    For example, the series `pd.Series([1.0, 2.0, 3.0])` is encoded as a sequence of
    floats but in reality they are all integers.

    Examples:
        >>> x = pd.Series([1.0, 2.0, 3.0])
        >>> relation = model_relation(tenzing_integer, tenzing_float)
        >>> relation.is_relation(x)
        True

        >>> relation.transform(x)
        pd.Series([1, 2, 3])
    """

    def __init__(self, model, friend_model, relationship=None, transformer=None):
        """
        Args:
            model: The type this relation will transform a series into.
            friend_model: The type this relation will transform a series from.
            relationship: A method to determine if a series of friend_model type can be converted to type model.
            transformer: A method to convert a series from type friend_model to type model.
        """
        self.model = model
        self.friend_model = friend_model
        self.conversion = relationship is not None or transformer is not None
        self.relationship = relationship if relationship else self.model.__contains__
        self.transformer = transformer

    def is_relation(self, obj) -> bool:
        return self.relationship(obj)

    def transform(self, obj):
        return self.model.cast(obj, self.transformer)

    def __repr__(self) -> str:
        return f"({self.friend_model} -> {self.model})"


class meta_model(type):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            return cls == tenzing_model
        return cls.contains_op(series)

    # TODO: raise exception on instantiation
    #     raise Exception("Cannot instantiate a type!")
    # TODO: automatic static ?
    # https://stackoverflow.com/questions/31953113/purely-static-classes-in-python-use-metaclass-class-decorator-or-something-e

    def __str__(cls) -> str:
        return f"{cls.__name__}"

    def __repr__(cls) -> str:
        return str(cls)

    def __add__(self, other):
        """
        Examples:
            >>> type_generic + infinite_generic
        """
        if not issubclass(other, tenzing_model):
            raise Exception(
                f"{other} must be sublcass of type tenzing_model, but is of type {type(other)}"
            )
        return MultiModel([self, other])

    # def __or__(self, other):
    #     """
    #     Examples:
    #         >>> type_generic | infinite_generic
    #     """
    #     return self + other
    #
    # def __getitem__(self, item):
    #     """
    #     Examples:
    #         >>> missing_generic[type_generic]
    #     """
    #     return item + self


# TODO: rename to partitioner
class MultiModel(metaclass=meta_model):
    def __init__(self, models: list):
        assert len(models) >= 2

        self.models = []
        for model in models:
            self.add_model(model)

    def __contains__(self, series: pd.Series):
        if series.empty:
            return False
        return self.contains_op(series)

    def add_model(self, model):
        if not issubclass(model, tenzing_model):
            raise Exception(
                f"{model} must be subclass of type tenzing_model, but is of type {type(model)}"
            )
        if model in self.models:
            raise Exception("Duplicate types not allowed")

        for m in self.models:
            if issubclass(model, m):
                raise Exception(f"Added model {m} is not allowed to be a subclass of another model ({model}).")

        self.models.append(model)

    def __add__(self, other):
        """
        Examples:
            >>> self + infinite_generic
        """
        self.add_model(other)
        return self

    def mask(self, series: pd.Series):
        mask = pd.Series([False] * len(series), name=series.name)
        for container in self.models:
            mask ^= container.mask(series)
        return mask

    def contains_op(self, series: pd.Series) -> bool:
        # Assert valid partitioning
        if not self.mask(series).all():
            return False

        for model in self.models:
            mask = model.mask(series)
            if not mask.any() or not series[model.mask(series)] in model:
                return False

        return True

    def __str__(self):
        return f"({', '.join([str(model) for model in self.models])})"

    def __repr__(self):
        return str(self)


class tenzing_model(metaclass=meta_model):
    """Abstract implementation of a tenzing type.

    Provides a common API for building custom tenzing datatypes. These can optionally
    be augmented with mixins from :mod:`tenzing.core.mixins`

    Examples:
        >>> class tenzing_datetime(tenzing_model):
        >>>     def contains_op(self, series):
        >>>         return pdt.is_datetime64_dtype(series)
        >>>
        >>>     def cast_op(self, series):
        >>>         return pd.to_datetime(series)
        >>>
    """

    _relations = {}

    @classmethod
    def __instancecheck__(mcs, instance) -> bool:
        if instance.__class__ is mcs:
            return True
        else:
            return isinstance(instance.__class__, mcs)

    @classmethod
    def get_relations(cls) -> dict:
        # TODO: move to __new__ or so?
        if cls.__name__ not in cls._relations:
            cls._relations[cls.__name__] = {}

        return cls._relations[cls.__name__]

    @classmethod
    def register_relation(cls, relation) -> None:
        if cls.__name__ not in cls._relations:
            cls._relations[cls.__name__] = {}

        assert (
            relation.friend_model not in cls._relations[cls.__name__]
        ), "Only one relationship permitted per type"
        cls._relations[cls.__name__][relation.friend_model] = relation

    @classmethod
    def cast(cls, series: pd.Series, operation=None):
        operation = operation if operation is not None else cls.cast_op
        return operation(series)

    @classmethod
    @abstractmethod
    def mask(cls, series: pd.Series) -> pd.Series:
        return pd.Series([True] * len(series))

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return cls.mask(series).all()

    @classmethod
    @abstractmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        pass
