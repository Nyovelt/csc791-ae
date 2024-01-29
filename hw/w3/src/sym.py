import math
from tricks import the
class SYM:
    def __init__(self, s=None, n=0):
        self.txt = s if s else " "
        self.at = n
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0

    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = self.has.get(x, 0) + 1
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self):
        e = 0
        for v in self.has.values():
            p = v / self.n
            e -= p * math.log(p, 2)
        return e

    def small(self):
        return 0
    
    def like(self, x, prior):
        return ((self.has.get(x, 0) + the.m * prior) / (self.n + the.m))

    def __str__(self):
        return (f"SYM(txt: {self.txt}, at: {self.at}, n: {self.n}, mode: {self.mode}, "
                f"most: {self.most}, has: {self.has})")
