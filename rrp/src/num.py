import math
from tricks import the

class NUM:
    def __init__(self, s=None, n=0):
        self.txt = s if s is not None else " "
        self.at = n
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = float("inf")
        self.lo = -float("inf")
        self.heaven = 0 if s and s.endswith('-') else 1

    def add(self, x):
        if x != "?":
            self.n += 1
            d = x - self.mu
            self.mu += d / self.n
            self.m2 += d * (x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else math.sqrt(self.m2 / (self.n - 1))

    def small(self):
        # Assuming `the.cohen` is a predefined variable elsewhere in your code.
        return the.cohen * self.div()

    def norm(self, x):
        if x == "?":
            return x
        return (x - self.lo) / (self.hi - self.lo + 1E-30)

    def dist(self, x, y):
        if x == "?" and y == "?":
            return 1
        x, y = self.norm(x), self.norm(y)
        if x == "?":
            x = 1 if y < 0.5 else 0
        if y == "?":
            y = 1 if x < 0.5 else 0
        return abs(x - y)

    def bin(self, x):
        # Assuming `the.bins` is a predefined variable elsewhere in your code.
        tmp = (self.hi - self.lo) / (the.bins - 1)
        return 1 if self.hi == self.lo else math.floor(x / tmp + 0.5) * tmp
