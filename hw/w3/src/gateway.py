import sys
from data import DATA
from tricks import the
from num import NUM
from sym import SYM
from collections import Counter




args = sys.argv[1:]
for i in range(len(args)):
    if args[i] == "-f" and i < len(args) - 1:
        the.file = args[i + 1]
    elif args[i] == "-t" and i < len(args) - 1:
        the.target = args[i + 1]
    elif args[i] == "-s" and i < len(args) - 1:
        the.seed = int(args[i + 1])

data = DATA(the.file)

# Task 1


def print_class_info(file_path):
    data = DATA(file_path)
    col_class = data.cols.all[-1]
    total_rows = sum(col_class.has.values())
    
    print(f"Class information for file: {file_path}")
    print("Class", "Count", "Percentage", sep='\t')

    for class_name, count in col_class.has.items():
        percentage = (count / total_rows) * 100
        print(class_name, count, f"{percentage:.2f}%", sep='\t')
if the.target == "task1":
    print_class_info(the.file)

# Task 2
def learn(data, row, my):
    # Increment the count of processed rows
    my["n"] += 1

    # Get the index of the class column from the data
    klass_at = data.cols.klass.at  # Assuming the 'klass' attribute in 'cols' points to the class column
    # Retrieve the class label for the current row
    klass = row.cells[klass_at]

    # If more than 10 rows have been processed, start classifying and updating the model
    if my["n"] > 10:
        # Increment the count of classification attempts
        my["tries"] += 1
        # Classify the current row and ignore the returned likelihood (_)
        classification, _ = row.likes(my["datas"])
        # Update the accuracy: increment if the classification matches the actual class
        my["acc"] += 1 if klass == classification else 0

    # Check if the class already has a corresponding DATA object; if not, create one
    if klass not in my["datas"]:
        my["datas"][klass] = DATA()  # Initialize DATA object; ensure DATA() can be initialized as required
    # Update the DATA object for the given class with the current row
    my["datas"][klass].add(row)

# Example usage:
# Assuming 'data' is an instance of DATA
# 'row' is an instance of ROW
# 'my' is a dictionary to keep track of learning statistics
if the.target == "task3":
    for k in range(1,4):
        for m in range(1,4):
            the.k = k
            the.m = m
            my = {"n": 0, "tries": 0, "acc": 0, "datas": {}}
            rows = data.rows  # Assuming `data.rows` gives a list of ROW objects
            for row in rows:
                learn(data, row, my)

            if my["tries"] > 0:
                accuracy = my["acc"] / my["tries"]
                print(f"Accuracy: {accuracy}")
