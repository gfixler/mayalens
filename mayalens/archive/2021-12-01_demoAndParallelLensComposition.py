import mayalens
import mayalens.common as mlc

#helper functions
const = lambda x: lambda _: x
comp2 = lambda f: lambda g: lambda x: f(g(x))
reverse = lambda xs: xs[::-1]
upper = lambda s: s.upper()

# simple usage of pair lenses
testVal = (("test", 0), False)
mlc._1(testVal)
mlc._2(testVal)

# pair lens composition
(mlc._1 | mlc._2)(testVal)
secondOfFirst = mlc._1 | mlc._2
secondOfFirst(testVal)

# more sample data
data = [(("foo", 42), False), (("bar", 23), True), (("baz", 17), False)]

# mapping the composed lens
map(secondOfFirst, data)
map(secondOfFirst.set(1000), data)

#mapping with composed modify
mulBy = lambda n: lambda x: x * n
times23 = mulBy(23)

map(secondOfFirst.modify(times23), data)

# some sample data
me = { "personal": { "fname": "Gary"
                   , "lname": "Fixler"
                   , "dob": (8, 18, 1977)
                   }
      , "financial": { "bank": "BOA" }
      }
you = { "personal": { "fname": "Alice"
                    , "lname": "Cromwell"
                    , "dob": (3, 3, 1952)
                    }
      , "financial": { "bank": "Fifth Ninth" }
      }

# LENS ON DICT VALUES
dval_get = lambda k: lambda d: d[k]
dval_set = lambda k: lambda v: lambda d: dict(filter(lambda (K, _): k != K, d.items()) + [(k, v)])
dval = lambda k: mlc.Lens(dval_get(k), dval_set(k))

dval("personal")(me)
fname = dval("personal") | dval("fname")
fname(me)
fname.set("Bob")(me)
fname.modify(reverse)(me)

# LENS ON DICT KEYS
dkey_get = lambda k: lambda d: {k: d[k]}.keys()[0] # raises appropriate error on missing key
dkey_set = lambda k: lambda K: lambda d: dict(filter(lambda (_k, _): k != _k, d.items()) + [(K, d[k])])
dkey = lambda k: mlc.Lens(dkey_get(k), dkey_set(k))

dobkey = dval("personal") | dkey("dob")
dobkey(me)
dobkey.set("DateOfBirth")(me)

# lens on year
year_get = lambda (_, __, y): y
year_set = lambda y: lambda (m, d, _): (m, d, y)
year = mlc.Lens(dobYear_get, dobYear_set)

# lens on my year
myYear = dval("personal") | dval("dob") | year
myYear(me)
myYear.set(1900)(me)

# lens on char in string
charAt_get = lambda n: lambda s: s[n]
charAt_set = lambda n: lambda c: lambda s: s[:n] + c + s[n:][1:]
charAt = lambda n: mlc.Lens(charAt_get(n), charAt_set(n))

charAt(3).modify(upper)("awesome")
charAt(3).modify(const("z"))("awesome")

# HOF for combining lenses in parallel
lenses2_get = lambda m: lambda n: lambda x: (m(x), n(x))
lenses2_set = lambda m: lambda n: lambda (a, b): lambda x: n.set(b)(m.set(a)(x))
lenses2 = lambda m: lambda n: mlc.Lens(lenses2_get(m)(n), lenses2_set(m)(n))

fnameFirstAndLast = dval("personal") | dval("fname") | lenses2(charAt(0))(charAt(-1))
fnameFirstAndLast(me)
fnameFirstAndLast.set(("B", "t"))(me)

# modify here requires mapping 2 functions into pair of values
onPairEach = lambda f: lambda g: lambda (x, y): (f(x), g(y))
fnameFirstAndLast.modify(onPairEach(const("Z"))(upper))(me)

