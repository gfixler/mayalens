# HELPER FUNCTIONS
comp2 = lambda f: lambda g: lambda x: f(g(x)) # 2 should be enough for anyone
cmap = lambda f: lambda xs: map(f, xs) # curried map

reverse = lambda xs: xs[::-1]
upper = lambda x: x.upper()
inc = lambda x: x + 1
add = lambda n: lambda x: x + n


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


# LENS ON FIRST ELEMENT OF PAIR
first_get = lambda (x, _): x
first_set = lambda v: lambda (x, y): (v, y)
first = Lens(first_get, first_set)

# LENS ON SECOND ELEMENT OF PAIR
second_get = lambda (_, y): y
second_set = lambda v: lambda (x, y): (x, v)
second = Lens(second_get, second_set)

# SIMPLE USAGE
first.get(("foo", 7)) # "foo"
first.set("bar")(("foo", 7)) # ("bar", 7)
makeFirstFalse = first.set(False) # premake a setter (just a setter function now, no longer a Lens)
makeFirstFalse((True, 7)) # (False, 7)
# map premade setter func over a list of pairs
cmap(makeFirstFalse)([(True, 7), (False, 3), (True, 42)])
# give a name to previous idea of Falsifying all first values in list
clearAll = cmap(makeFirstFalse)
clearAll(([(True, 7), (False, 3), (True, 42)])) # same as cmap example above

# LENS ON ELEMENT OF LIST
nth_get = lambda n: lambda xs: xs[n]
nth_set = lambda n: lambda v: lambda xs: xs[:n] + [v] + xs[n+1:]
nth = lambda n: Lens(nth_get(n), nth_set(n))

# SIMPLE USAGE
xs = [1, 2, 3, 4, 5] # list example
nth(0).get() # 1
nth(2).set(7)(xs) # [1, 2, 7, 4, 5]
nth(3).modify(add(5))(xs) # [1, 2, 3, 9, 5]

# COMPOSE LENSES
(first | second).get(((False, "foo"), 7)) # get
(first | second).set("bar")(((False, "foo"), 7)) # set
(first | second).modify(reverse)(((False, "foo"), 7)) # modify

# LENS ON DICTS
key_get = lambda k: lambda d: d[k]
key_set = lambda k: lambda v: lambda d: dict(filter(lambda (K, _): k != K, d.items()) + [(k, v)])
key = lambda k: Lens(key_get(k), key_set(k))

# sample data
gameState = {"chars": {"Eve": {"hp": (97, 100)}, "Bob": {"hp": (57, 120)}}, "currentLevel": 2}

# premade modifier (no longer a Lens)
bumpLevel = key("currentLevel").modify(inc)
bumpLevel(gameState) # increments currentLevel from 2 to 3

# composed key Lenses
healthEve = key("chars") | key("Eve") | key("hp")
healthEve.get(gameState) # (97, 100)
# compose another Lens onto previous composition of Lenses (from dict into tuple)
maxHealthEve = healthEve | second
maxHealthEve.get(gameState) # 100
# compose Lens' modify method to create helper function (no longer a Lens)
bumpMaxHealthEveBy = comp2(maxHealthEve.modify)(add)
bumpMaxHealthEveBy(20)(gameState) # Eve's max health raised from 100 to 120

