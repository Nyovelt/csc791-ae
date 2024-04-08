import math
from tricks import the
import l

class RANGE:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {'lo': lo, 'hi': hi if hi is not None else lo}
        self.y = {}

    def add(self, x, y):
        self.x['lo'] = min(self.x['lo'], x)
        self.x['hi'] = max(self.x['hi'], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(self):
        lo, hi, s = self.x['lo'], self.x['hi'], self.txt
        if lo == -math.inf:
            return f"{s} < {hi}"
        if hi == math.inf:
            return f"{s} >= {lo}"
        if lo == hi:
            return f"{s} == {lo}"
        return f"{lo} <= {s} < {hi}"

    def score(self, goal, LIKE, HATE):
        # Placeholder for scoring function
        pass

    def merge(self, other):
        both = RANGE(self.at, self.txt, min(self.x['lo'], other.x['lo']))
        both.x['hi'] = max(self.x['hi'], other.x['hi'])
        for t in [self.y, other.y]:
            for k, v in t.items():
                both.y[k] = both.y.get(k, 0) + v
        return both

    def merged(self, other, tooFew):
        both = self.merge(other)
        e1, n1 = l.entropy(self.y)  # Assume entropy function exists
        e2, n2 = l.entropy(other.y)
        if n1 <= tooFew or n2 <= tooFew or l.entropy(both.y) <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both

def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range in _ranges1(col, rowss):
            t.append(range)
    return t

def _ranges1(col, rowss):
    out, nrows = {}, 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in rows:
            x = row.cells[col.at]
            if x != "?":
                bin = col.bin(x)  # Assuming a binning function exists on col
                if bin not in out:
                    out[bin] = RANGE(col.at, col.txt, x)
                out[bin].add(x, y)
    sorted_out = sorted(out.values(), key=lambda r: r.x['lo'])
    return _mergeds(sorted_out, nrows / the.bins) if col.has else sorted_out  

def _mergeds(ranges, tooFew):
    i, t = 1, []
    while i <= len(ranges):
        a = ranges[i - 1]
        if i < len(ranges):
            both = a.merged(ranges[i], tooFew)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return _mergeds(t, tooFew)
    for i in range(1, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    t[0].x['lo'], t[-1].x['hi'] = -math.inf, math.inf
    return t



# Note: This code assumes the presence of classes or functions not fully detailed in the snippet.
# - The `entropy` function needs to be defined.
# - The `bin` method in col objects and how they're structured and used is assumed to exist.
# - Global variable `the.bins` is referenced, assuming it defines the number of bins to use.
