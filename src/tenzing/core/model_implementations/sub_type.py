from abc import abstractmethod


class SubTypeMeta(type):
    def __contains__(cls, item):
        return cls.contains_op(item)

    def __repr__(self):
        return f"{self.__name__}"


class subType(object, metaclass=SubTypeMeta):
    """subTypes are composable extensions to types (e.g. NaN and Inf)"""

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def get_mask(series):
        pass

    @staticmethod
    def contains_op(series):
        return True

