from cols import COLS
from row import ROW
import l 

class DATA:
    def __init__(self, src=None, fun=None):
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            # Assuming l.csv is a method to parse CSV files
            for x in l.csv(src):
                self.add(x, fun)
        else:
            for x in (src or []):
                self.add(x, fun)

    def add(self, t, fun=None):
        row = t if hasattr(t, 'cells') else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)
    def print(self):
        print(self.cols)
        for row in self.rows:
            row.print()

    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def small(self):
        u = [col.small() for col in self.cols.all]
        return ROW(u)

    def stats(self, cols=None, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        target_cols = self.cols[cols or "y"]
        for col in target_cols.values():
            col_function = getattr(col, fun or "mid")
            u[col.txt] = l.rnd(col_function(), ndivs)
        return u


    def gate(self, budget0, budget, some):
        stats, bests = {}, {}
        rows = l.shuffle(self.rows)  # Assuming l.shuffle is a predefined function
        lite, dark = rows[:budget0], rows[budget0:]
        for i in range(1, budget + 1):
            best, rest = self.bestRest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            stats[i] = selected.mid()
            bests[i] = best.rows[0]
            lite.append(dark.pop(todo))
        return stats, bests

    def split(self, best, rest, lite, dark):
        selected = DATA({'cols.names': self.cols.names})
        max_val = float('inf')
        out = 1
        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b + r) / abs(b - r + 1e-300)
            if tmp > max_val:
                out, max_val = i, tmp
        return out, selected

    def bestRest(self, rows, want):
        rows.sort(key=lambda a: a.d2h(self))
        best = DATA({'cols.names': self.cols.names})
        rest = DATA({'cols.names': self.cols.names})
        for i, row in enumerate(rows):
            if i < want:
                best.add(row)
            else:
                rest.add(row)
        return best, rest
