from tricks import the
import math

class NUM:
    def __init__(self, s=None, n=0):
        self.txt = s if s else " "
        self.at = n
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = -float('inf')
        self.lo = float('inf')
        self.heaven = 0 if (s or "").endswith("-") else 1

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
        return 0 if self.n < 2 else (self.m2 / (self.n - 1)) ** 0.5

    def small(self):
        # Assuming 'the' is an external object with an attribute 'cohen'
        return the.cohen * self.div()

    def norm(self, x):
        if x == "?":
            return x
        else:
            return (x - self.lo) / (self.hi - self.lo + 1E-30)
        
    def like(self, x, _unused=None):
        if x == "?":
            return 0
        sd = self.div() + 1E-30
        mu = self.mid()
        nom = math.exp(-0.5 * ((x - mu) ** 2) / (sd ** 2))
        denom = sd * math.sqrt(2 * math.pi)
        return nom / denom

    def __str__(self):
        return (f"NUM(txt: {self.txt}, at: {self.at}, n: {self.n}, mu: {self.mu:.2f}, "
                f"m2: {self.m2:.2f}, hi: {self.hi}, lo: {self.lo}, "
                f"heaven: {self.heaven}, div: {self.div():.2f})")
