from itertools import combinations, chain
import l
from rule import RULE
from tricks import the
class RULES:
    def __init__(self, ranges, goal, rowss):
        self.sorted = []
        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0
        self.likeHate()
        for range in ranges:
            range.scored = self.score(range.y)
        self.sorted = self.top(self.try_(self.top(ranges)))

    def likeHate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return l.score(t, self.goal, self.LIKE, self.HATE)
    def try_(self, ranges):
        u = []
        # Generate all non-empty subsets of ranges
        for r in range(1, len(ranges) + 1):
            for subset in combinations(ranges, r):
                rule = RULE(list(subset))
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        # Sort the rules based on their scored attribute
        t.sort(key=lambda x: x.scored, reverse=True)
        # Assuming 'the.Cut' and 'the.Beam' are predefined values controlling filtering and slicing
        u = [x for x in t if x.scored >= t[0].scored * the.Cut]
        return u[:the.Beam]
