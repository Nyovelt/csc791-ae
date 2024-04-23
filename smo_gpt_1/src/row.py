import math
from tricks import the

class ROW:
    def __init__(self, t):
        self.cells = t

    def __repr__(self):
        return f"ROW(cells: {self.cells})"

    def __str__(self):
        return f"ROW(cells: {self.cells})"

    def d2h(self, data):
        d, n = 0, 0
        for col in data.cols.y.values():
            n += 1
            d += abs(col.heaven - col.norm(self.cells[col.at])) ** 2
        return (d ** 0.5) / (n ** 0.5)

    def likes(self, datas):
        n, nHypotheses, most, out = 0, 0, None, None
        for data in datas.values():
            n += len(data.rows)
            nHypotheses += 1
        for key, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, key
        # print(f"Row classified as: {out} with likelihood: {most}")
        return out, most

    def like(self, data, n, nHypotheses):
        if the.k is None:
            the.k = 1
        prior = (len(data.rows) + the.k) / (n + the.k * nHypotheses)
        out = math.log(prior)
        for col in data.cols.x.values():
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior) + 1e-10
                out += math.log(inc)
        return math.exp(out)
