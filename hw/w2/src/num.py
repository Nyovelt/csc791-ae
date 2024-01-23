from tricks import the

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
    
    
