class Lens (object):
    """
    Based loosely on the first 6 pages of this paper:
    Understanding Profunctor Optics: a representation theorem
    Guillaume Boisseau, St Anne's College, University of Oxford
    https://arxiv.org/pdf/2001.11816.pdf
    """

    def __init__ (self, getter, setter):
        """
        getter and setter each target the same element of a structure

        getter is a function that takes the structure and returns the element

        setter is a function that takes a value, and returns a function which
        takes the structure, and returns a copy, with the element replaced by
        the value

        Example Lens onto the first element in a 2-tuple:

        first_get = lambda (x, _): x
        first_set = lambda v: lambda (x, y): (v, y)
        first = Lens(first_get, first_set)
        """
        self.get = getter
        self.set = setter

    def modify (self, f):
        return lambda s: self.set(f(self.get(s)))(s)

    def __or__ (self, other):
        """
        Compose Lenses with the pipe char.

        Example:

        compositeLens = lensA | lensB | lensC
        """
        composedGet = comp2(other.get)(self.get)
        composedSet = lambda v: lambda s: self.set(other.set(v)(self.get(s)))(s)
        return Lens(composedGet, composedSet)

