class Lens (object):
    """
    Based loosely on the first 6 pages of this paper:
    Understanding Profunctor Optics: a representation theorem
    Guillaume Boisseau, St Anne's College, University of Oxford
    https://arxiv.org/pdf/2001.11816.pdf
    """

    def __init__ (self, getter, setter):
        self.get = getter
        self.set = setter

    def modify (self, f):
        return lambda s: self.set(f(self.get(s)))(s)

    def __or__ (self, other):
        """
        Compose Lenses with the pipe char.
        """
        composedGet = comp2(other.get)(self.get)
        composedSet = lambda v: lambda s: self.set(other.set(v)(self.get(s)))(s)
        return Lens(composedGet, composedSet)

