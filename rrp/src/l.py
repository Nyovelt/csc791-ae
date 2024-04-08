import random
import math
import sys
import re

def powerset(s):
    t = [[]]
    for item in s:
        t += [x + [item] for x in t]
    return t

def as_list(t):
    return list(t.values())

def entropy(t):
    n = sum(t.values())
    e = -sum(v / n * math.log2(v / n) for v in t.values())
    return e, n


def any(t):
    return random.choice(t)


def many(t, n=None):
    n = n or len(t)
    return [any(t) for _ in range(n)]


def keys(t):
    return sorted(t.keys())


def copy(t):
    if not isinstance(t, dict):
        return t
    return {copy(k): copy(v) for k, v in t.items()}


def shuffle(t):
    u = list(t)
    random.shuffle(u)
    return u


def slice(t, start=None, stop=None, step=None):
    return t[slice(start, stop, step)]

def keysort(t, fun):
    return [x for x, _ in sorted(t.items(), key=lambda item: fun(item[1]))]


def coerce(s):
    if s.isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        if s.lower() == "true":
            return True
        elif s.lower() == "false":
            return False
        else:
            return s.strip()


def settings(s):
    t = {}
    pat = r"--(\S+)= (\S+)"
    for k, s1 in re.findall(pat, s):
        t[k] = coerce(s1)
    t['_help'] = s
    return t

def cells(s):
    return [coerce(item) for item in s.split(',')]


def csv(src):
    def generator():
        with open(src, 'r') if src != "-" else sys.stdin as f:
            for line in f:
                yield cells(line)
    return generator()


def cli(t):
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg.startswith("--"):
            k = arg[2:]
            if k in t and i + 1 < len(args):
                t[k] = coerce(args[i + 1])
        elif arg.startswith("-"):
            k = arg[1:]
            if k in t:
                t[k] = not t[k]
    if t.get('help', False):
        print("\n" + t['_help'])
        sys.exit()
    return t

def fmt(format_string, *args):
    """Emulate sprintf"""
    return format_string % args

def oo(x):
    """Print a string of a nested structure and return the structure."""
    print(o(x))
    return x

def o(t, n=None):
    """Return a string for a nested structure."""
    if isinstance(t, (int, float)):
        return str(np.round(t, n) if n is not None else t)
    if not isinstance(t, dict):
        return str(t)
    u = []
    for k in sorted(t.keys()):
        if str(k).startswith("_"):
            continue
        if isinstance(t, dict):
            u.append(f"{o(k, n)}: {o(t[k], n)}" if isinstance(t[k], dict) else f"{o(k, n)}: {o(t[k], n)}")
        else:
            u.append(o(t[k], n))
    return "{" + ", ".join(u) + "}"
