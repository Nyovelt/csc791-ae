import sys
from data import DATA
from tricks import the
from num import NUM
from sym import SYM

# Read and process the CSV file
data = DATA("../data/auto93.csv")

args = sys.argv[1:]
for i in range(len(args)):
    if args[i] == "-f" and i < len(args) - 1:
        the.file = args[i + 1]
    elif args[i] == "-t" and i < len(args) - 1:
        the.target = args[i + 1]
    elif args[i] == "-s" and i < len(args) - 1:
        the.seed = int(args[i + 1])

stats = {}
stats[".N"] = len(data.rows)
for col in data.cols.all:
    if isinstance(col, NUM):
        # Assuming NUM class has methods to calculate mean (mu)
        stats[col.txt] = col.mu
    elif isinstance(col, SYM):
        # Assuming SYM class has a method to calculate mode (mode)
        stats[col.txt] = col.mode

print(stats)


