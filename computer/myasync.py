def coroutine(f):
    def decorator(*args, **kwargs):
        return Coroutine(f(*args, **kwargs))
    return decorator

class Coroutine:
    def __init__(self, gen):
        self.__iter__ = self.__gen = gen
        self.__next__ = self.__call__
    def __call__(self):
        next(self.__gen)
class Loop(Coroutine):
    _coroutines = []
    def __init__(self):
        super().__init__(self.__f)

    def __f(self):
        while 1:
            new_coroutines = []
            for coroutine in self.coroutines:
                try:
                    coroutine()
                except StopIteration:
                    pass
                else:
                    new_coroutines.append(coroutine)
            self._coroutines = new_coroutines
            yield
                
def run(coroutine):
    while 1:
        try:
            coroutine.__next__()
        except StopIteration:
            return