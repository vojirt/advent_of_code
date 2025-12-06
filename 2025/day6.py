import numpy as np


def parse_data(data):
    arr = []
    for line in data: 
        arr.append([s for s in line.split(' ') if len(s) > 0])
    return np.array(arr[:-1]).astype(int), arr[-1]

def part1(numbers, op):
    acc = 0
    for i,o in enumerate(op):
        if o == "*":
            acc += np.prod(numbers[:, i])
        else:
            # + 
            acc += np.sum(numbers[:, i])
    return acc

def part2(data):
    arr = [""]*len(data[0])
    for i in range(0, len(data)-1): 
        for j in range(0, len(arr)):
            arr[j] += data[i][j] 
    arr = np.array([a.strip(" ") for a in arr])
    op = ([s for s in data[-1].split(' ') if len(s) > 0])

    acc = 0
    prev_idd = 0
    idd_list = np.nonzero(arr=='')[0].tolist() + [len(arr)]
    for i, idd in enumerate(idd_list):
        if op[i] == "*":
            acc += np.prod(arr[prev_idd:idd].astype(int))
        else:
            # + 
            acc += np.sum(arr[prev_idd:idd].astype(int))
        prev_idd = idd+1

    return acc


if __name__ == "__main__":
    data = [
"123 328  51 64 ", 
" 45 64  387 23 ",
"  6 98  215 314",
"*   +   *   + "]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    # numbers, op = parse_data(data)
    # result = part1(numbers, op)
    # assert result == 4277556, f"{result}"

    result = part2(data)
    assert result == 3263827, f"{result}"
