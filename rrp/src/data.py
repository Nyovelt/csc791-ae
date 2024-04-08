import csv
from row import ROW
from cols import COLS
import random
from node import NODE
from tricks import the

class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None
        # If src is a string, assume it's a filename and load from CSV
        if isinstance(src, str):
            with open(src, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.add(row, fun)
        # Otherwise, assume src is a list of rows
        else:
            for row in src or []:
                self.add(row, fun)

    def add(self, t, fun=None):
        row = t if isinstance(t, ROW) else ROW(t)
        if self.cols:
            # Optionally apply a function before adding the row
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def small(self):
        u = [col.small() for col in self.cols.all]
        return ROW(u)

    def stats(self, cols='y', fun='mid', ndivs=None):
        u = {'.N': len(self.rows)}
        for col in self.cols[cols]:
            # Assuming `l.rnd` and the method access via `getattr` is correctly replicated in Python context
            u[col.txt] = round(getattr(col, fun)(), ndivs) if ndivs else getattr(col, fun)()
        return u

    def clone(self, rows=None):
        new_data = DATA([self.cols.names])
        for row in rows or []:
            new_data.add(row)
        return new_data

    def far_apart(self, rows, sortp, a=None, b=None, far=None, evals=0):
            far = int(len(rows) * the.Far)
            evals = 1 if a else 2
            a = a or random.choice(rows).neighbors(self, rows)[far]
            b = a.neighbors(self, rows)[far]
            if sortp and b.d2h(self) < a.d2h(self):
                a, b = b, a
            return a, b, a.dist(b, self), evals

    def half(self, rows, sortp, before=None, evals=0):
        some = random.sample(rows, min(the.Half, len(rows)))
        a, b, C, evals = self.far_apart(some, sortp, before)
        def d(row1, row2): return row1.dist(row2, self)
        def project(r): return (d(r, a) ** 2 + C ** 2 - d(r, b) ** 2) / (2 * C)
        rows_sorted = sorted(rows, key=project)
        midpoint = len(rows) // 2
        as_, bs = rows_sorted[:midpoint], rows_sorted[midpoint:]
        return as_, bs, a, b, C, d(a, bs[0]), evals

    def tree(self, sortp):
        evals = 0

        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows) > 2 * (len(self.rows) ** 0.5):
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = \
                    self.half(data.rows, sortp, above)
                evals += evals1
                node.lefts = _tree(DATA(lefts), node.left)
                node.rights = _tree(DATA(rights), node.right)
            return node

        return _tree(self), evals

    def branch(self, stop=None):
        evals, rest = 1, []
        stop = stop or (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals
            if len(data.rows) > stop:
                lefts, rights, left = self.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(DATA(lefts), left)
            else:
                return DATA(data.rows), DATA(rest), evals

        return _branch(self)
