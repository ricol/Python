#!/usr/bin/env python
#-*- coding: utf-8 -*-

def f(*args,  ** kwargs):
    print(args, kwargs)

l = [1, 2, 3]
t = (4, 5, 6)
d = {'a':7, 'b':8, 'c':9}

f()
f(1, 2, 3)                    # (1, 2, 3) {}
f(1, 2, 3, "groovy")           # (1, 2, 3, 'groovy') {}
f(a=1, b=2, c=3)              # () {'a': 1, 'c': 3, 'b': 2}
f(a=1, b=2, c=3, zzz="hi")     # () {'a': 1, 'c': 3, 'b': 2, 'zzz': 'hi'}
f(1, 2, 3, a=1, b=2, c=3)        # (1, 2, 3) {'a': 1, 'c': 3, 'b': 2}

f(*l,  ** d)                   # (1, 2, 3) {'a': 7, 'c': 9, 'b': 8}
f(*t,  ** d)                   # (4, 5, 6) {'a': 7, 'c': 9, 'b': 8}
f(1, 2, *t)                   # (1, 2, 4, 5, 6) {}
f(q="winning",  ** d)          # () {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}
f(1, 2, *t, q="winning",  ** d)   # (1, 2, 4, 5, 6) {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}

def f2(arg1, arg2, *args,  ** kwargs):
    print arg1, arg2, args, kwargs

f2(1, 2, 3)                       # 1 2 (3,) {}
f2(1, 2, 3, "groovy")              # 1 2 (3, 'groovy') {}
f2(arg1=1, arg2=2, c=3)           # 1 2 () {'c': 3}
f2(arg1=1, arg2=2, c=3, zzz="hi")  # 1 2 () {'c': 3, 'zzz': 'hi'}
f2(1, 2, 3, a=1, b=2, c=3)           # 1 2 (3,) {'a': 1, 'c': 3, 'b': 2}

f2(*l,  ** d)                   # 1 2 (3,) {'a': 7, 'c': 9, 'b': 8}
f2(*t,  ** d)                   # 4 5 (6,) {'a': 7, 'c': 9, 'b': 8}
f2(1, 2, *t)                   # 1 2 (4, 5, 6) {}
f2(1, 1, q="winning",  ** d)      # 1 1 () {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}
f2(1, 2, *t, q="winning",  ** d)   # 1 2 (4, 5, 6) {'a': 7, 'q': 'winning', 'c': 9, 'b': 8}