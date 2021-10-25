comp2 = lambda f: lambda g: lambda x: f(g(x))


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

    def __call__ (self, x):
        return self.get(x)

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


class ImpureLens (Lens):
    """
    Impure lenses are meant for values that don't pull apart and go back
    together like the values in typical, pure lenses. An example would be a
    setting in a tool or program that's locked, and holds its value through
    attempts to set it. For these values, the only reliable way to return the
    new value is to get it again, after setting it. That's what this class
    does. It derives from Lens, and simply overrides the init method to wrap
    the setter passed in, such that after it sets, it calls the passed-in
    getter again, and returns the value it receives.
    """
    def __init__ (self, getter, setter):
        self.get = getter
        self.set = lambda v: lambda x: [setter(v)(x), getter(x)][1]

