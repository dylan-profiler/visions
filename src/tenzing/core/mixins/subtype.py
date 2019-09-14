from abc import abstractmethod


class subtype_mixin:
    @abstractmethod
    @staticmethod
    def mask(self, series):
        pass
