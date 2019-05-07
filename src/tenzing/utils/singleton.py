from abc import ABCMeta


class Singleton(ABCMeta):
    """Singleton metaclass

    Any instantiation of a Singleton class yields
    the exact same object, e.g.

    >>> class MyClass(metaclass=Singleton):
    >>>     pass
    >>> a = MyClass()
    >>> b = MyClass()
    >>> a is b
    True
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def __instancecheck__(mcs, instance):
        if instance.__class__ is mcs:
            return True
        else:
            return isinstance(instance.__class__, mcs)


def singleton_object(cls):
    """Singleton metaclass class decorator.

    This class decorator transforms (and replaces) a class definition (which
    must have a Singleton metaclass) with the actual singleton object.


    >>> @singleton_object
    >>> class MySingleton(metaclass=Singleton):
    >>>     pass
    >>> MySingleton is MySingleton() # Doesn't require instantiation
    True
    """
    assert isinstance(cls, Singleton), cls.__name__ + " must use Singleton metaclass"

    def self_instantiate(self):
        return self

    cls.__call__ = self_instantiate
    cls.__hash__ = lambda self: hash(cls)
    cls.__repr__ = lambda self: cls.__name__
    cls.__reduce__ = lambda self: cls.__name__
    obj = cls()
    obj.__name__ = cls.__name__
    return obj
