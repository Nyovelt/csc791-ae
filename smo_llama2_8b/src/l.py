import math
import random
import csv
import tricks
import re

b4={}

def rogues():
    for k, v in globals().items():
        if k not in b4:
            print("E:", k, type(k))

def rnd(n, ndecs=2):
    if not isinstance(n, (int, float)):
        return n
    return round(n, ndecs)

def keys(t):
    return sorted(t.keys())

def copy(t):
    if not isinstance(t, dict):
        return t
    return {copy(k): copy(v) for k, v in t.items()}

def shuffle(t):
    u = t[:]
    random.shuffle(u)
    return u

def slice(t, go, stop, inc=1):
    return t[go:stop:inc]

def settings(s):
    t = {}
    pat = r"--([^\s]+)[^\=]+= ([^\s]+)"
    for k, v in re.findall(pat, s):
        t[k] = tricks.coerce(v)
    t['_help'] = s
    return t

def cells(s):
    return [tricks.coerce(item) for item in s.split(',')]

def csv(src):
    if src == "-":
        file = sys.stdin
    else:
        file = open(src, 'r')
    for line in file:
        yield cells(line)
    file.close()
    
def cli(t, args):
    for k, v in t.items():
        v = str(v)
        for i, arg in enumerate(args):
            if arg == f"-{k[0]}" or arg == f"--{k}":
                next_val = args[i + 1] if i + 1 < len(args) else None
                t[k] = coerce(next_val if next_val else not bool(v))
    if t.get("help"):
        sys.exit(print(t.get("_help")))
    return t


