import sys
from data import DATA
from tricks import the
from num import NUM
from sym import SYM
from collections import Counter
import random
import math


args = sys.argv[1:]
for i in range(len(args)):
    if args[i] == "-f" and i < len(args) - 1:
        the.file = args[i + 1]
    elif args[i] == "-t" and i < len(args) - 1:
        the.target = args[i + 1]
    elif args[i] == "-s" and i < len(args) - 1:
        the.seed = int(args[i + 1])

data = DATA(the.file)

def eg_gate():
    budget0, budget, some = 4, 10, 0.5
    print(the.seed)
    d = data
    def sayd(row, txt):
        print(row)
        print(format(row), txt, round(row.d2h(d), 2))

    def say(row, txt):
        print(format(row.cells), txt)

    print(format(d.cols.names), "about", "d2h")
    print("#overall" + "-"*37)
    sayd(d.mid(), "mid")
    say(d.div(), "div")
    say(d.small(), "small=div*" + str(the.cohen))
    
    print("#generality" + "-"*37)
    stats, bests = d.gate(budget0, budget, some)
    for i, stat in stats.items():
        sayd(stat, i + budget0)


    print("#specifically" + "-"*63)
    for i, best in bests.items():
        sayd(best, i + budget0)

    print("#optimum" + "-"*63)
    d.rows.sort(key=lambda a: a.d2h(d))
    sayd(d.rows[0], len(d.rows))

    print("#random" + "-"*63)
    rows = random.sample(d.rows, len(d.rows))
    rows = rows[:int(math.log(0.05) / math.log(1 - the.cohen / 6))]
    rows.sort(key=lambda a: a.d2h(d))
    sayd(rows[0], "")

# eg_gate()

def eg_gate20():
    print("#best, mid")
    for i in range(20):
        d = data
        stats, bests = d.gate(4, 16, 0.5)

        if stats and bests:  # Check if 'stats' and 'bests' have entries
            # Access the last item inserted into the dictionary
            last_stat_key = list(stats.keys())[-1]
            last_best_key = list(bests.keys())[-1]
            stat = stats[last_stat_key]
            best = bests[last_best_key]
            print("5. best "+ str(round(best.d2h(d), 2)) + "\n" "6. mid " + str(round(stat.d2h(d), 2)))
        else:
            print("No data in stats or bests")

eg_gate20()
