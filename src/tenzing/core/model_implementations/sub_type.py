from abc import abstractmethod


class SubTypeMeta(type):
    def __contains__(cls, item):
        return cls.contains_op(item)

    def __str__(self):
        return f"{self.__name__}"

    def __repr__(self):
        return str(self)


class subType(object, metaclass=SubTypeMeta):
    """subTypes are composable extensions to types (e.g. NaN and Inf)"""

    @staticmethod
    @abstractmethod
    def get_mask(series):
        pass

    @staticmethod
    def contains_op(series):
        return True
