class Singleton:

    def __init__(self, _cls):
        """
        Decorator class to implement the "singleton" design pattern.
        :param _cls: Class to apply the the singleton pattern to.
        """
        self._cls = _cls
        self._instance = None

    def __call__(self, *args, **kwds):
        if self._instance is None:
            self._instance = self._cls(*args, **kwds)
        return self._instance
