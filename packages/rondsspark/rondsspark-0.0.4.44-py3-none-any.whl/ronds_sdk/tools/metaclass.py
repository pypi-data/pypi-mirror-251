

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaCollector(type):

    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        setattr(instance, '__init_args', args)
        setattr(instance, '__init_kwargs', kwargs)
        return instance
