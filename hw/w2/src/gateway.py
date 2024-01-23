import sys
from data import DATA
from tricks import the
from num import NUM
from sym import SYM

# Read and process the CSV file
data = DATA("../data/auto93.csv")

stats = {}
for col in data.cols.all:
    if isinstance(col, NUM):
        # Assuming NUM class has methods to calculate mean (mu)
        stats[col.txt] = col.mu
    elif isinstance(col, SYM):
        # Assuming SYM class has a method to calculate mode (mode)
        stats[col.txt] = col.mode

print(stats)


