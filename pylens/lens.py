class Lens (object):
    """
    Based loosely on the first 6 pages of this paper:
    Understanding Profunctor Optics: a representation theorem
    Guillaume Boisseau, St Anne's College, University of Oxford
    https://arxiv.org/pdf/2001.11816.pdf
    """

    def __init__ (self, getter, setter):
        self._get = getter
        self._set = setter

    def get (self, structure):
        return self._get(structure)

    def set (self, value):
        return self._set(value)

    def modify (self, f):
        return lambda s: self._set(f(self._get(s)))(s)

    def __or__ (self, other):
        """
        Compose Lenses with the pipe char.
        """
        composedGet = comp2(other._get)(self._get)
        # from paper: put y s = put1 (put2 y (get1 s)) s
        composedSet = lambda v: lambda s: self._set(other._set(v)(self._get(s)))(s)
        return Lens(composedGet, composedSet)

