from .lens import Lens


# LENS ON FIRST ELEMENT OF PAIR
_1_get = lambda (x, _): x
_1_set = lambda v: lambda (x, y): (v, y)
_1 = Lens(_1_get, _1_set)

# LENS ON SECOND ELEMENT OF PAIR
_2_get = lambda (_, y): y
_2_set = lambda v: lambda (x, y): (x, v)
_2 = Lens(_2_get, _2_set)

# LENS ON ELEMENT OF LIST
nth_get = lambda n: lambda xs: xs[n]
nth_set = lambda n: lambda v: lambda xs: xs[:n] + [v] + xs[n + 1:]
nth = lambda n: Lens(nth_get(n), nth_set(n))

# LENS ON CHARACTER IN STRING
charAt_get = lambda n: lambda s: s[n]
charAt_set = lambda n: lambda v: lambda s: s[:n] + v + s[n + 1:]
charAt = lambda n: Lens(charAt_get(n), charAt_set(n))

# LENS ON DICT KEYS
dkey_get = lambda k: lambda d: {k: d[k]}.keys()[0] # raises appropriate error on missing key
dkey_set = lambda k: lambda K: lambda d: dict(filter(lambda (_k, _): k != _k, d.items()) + [(K, d[k])])
dkey = lambda k: Lens(dkey_get(k), dkey_set(k))

# LENS ON DICT VALUES
dval_get = lambda k: lambda d: d[k]
dval_set = lambda k: lambda v: lambda d: dict(filter(lambda (K, _): k != K, d.items()) + [(k, v)])
dval = lambda k: Lens(dval_get(k), dval_set(k))

