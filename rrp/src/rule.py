class RULE:
    def __init__(self, ranges):
        self.parts = {}
        self.scored = 0
        for range in ranges:
            if range.txt not in self.parts:
                self.parts[range.txt] = []
            self.parts[range.txt].append(range)

    def _or(self, ranges, row):
        x = row.cells[ranges[0].at]
        if x == "?":
            return True
        for range in ranges:
            lo, hi = range.x['lo'], range.x['hi']
            if lo == hi and lo == x or lo <= x and x < hi:
                return True
        return False

    def _and(self, row):
        for ranges in self.parts.values():
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        selected_rows = []
        for row in rows:
            if self._and(row):
                selected_rows.append(row)
        return selected_rows

    def selectss(self, rowss):
        result = {}
        for y, rows in rowss.items():
            result[y] = len(self.selects(rows))
        return result

    def show(self):
        ands = []
        for ranges in self.parts.values():
            ors = show_less(ranges)
            ors_texts = [range.show() for range in ors]
            ands.append(" or ".join(ors_texts))
        return " and ".join(ands)

def show_less(ranges, ready=False):
    if not ready:
        ranges = sorted(ranges, key=lambda r: r.x['lo'])
    i, u = 0, []
    while i < len(ranges):
        a = ranges[i]
        if i + 1 < len(ranges) and a.x['hi'] == ranges[i + 1].x['lo']:
            a = a.merge(ranges[i + 1])
            i += 1
        u.append(a)
        i += 1
    return u if len(u) == len(ranges) else show_less(u, True)

# Assuming a `RANGE` class exists that includes:
# - A constructor that takes `at`, `txt`, `lo`, `hi` (optional).
# - A `merge` method that combines two `RANGE` instances.
# - A `show` method that returns a string representation of the range.
