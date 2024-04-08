import math
import sys

class ROW:
    def __init__(self, cells):
        self.cells = cells

    def d2h(self, data):
        d, n, p = 0, 0, 2
        for col in data['cols']['y']:
            x = self.cells[col['at']]
            if x is None:
                print("?", file=sys.stderr)
            else:
                n += 1
                d += abs(col['heaven'] - col['norm'](self.cells[col['at']])) ** p
        return (d / n) ** (1 / p)

    def dist(self, other, data):
        d, n, p = 0, 0, data['the']['p']
        for col in data['cols']['x']:
            n += 1
            d += col['dist'](self.cells[col['at']], other.cells[col['at']]) ** p
        return (d / n) ** (1 / p)

    def neighbors(self, data, rows=None):
        rows = rows or data['rows']
        return sorted(rows, key=lambda row: self.dist(row, data))

