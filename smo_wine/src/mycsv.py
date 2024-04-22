import num

def read_csv(filepath):
    with open(filepath) as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines]

def process_csv(data):
    num_cols = len(data[0])
    num_objs = [num.NUM() for _ in range(num_cols)]
    
    header = data[0]
    data = data[1:]
    
    for row in data:
        for i in range(num_cols):
            num_objs[i].add(row[i])

    return header, num_objs
