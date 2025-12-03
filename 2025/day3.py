import numpy as np

def part1(data):
    acc = 0
    for bank in data:
        max_v1 = np.argmax(bank[:-1])
        max_v2 = np.max(bank[max_v1+1:])
        acc += int(str(bank[max_v1])+str(max_v2))
    return acc

def part2(data):
    acc = 0
    for bank in data:
        joltage = ""
        start = 0
        for i in range(0, 12):
            end = len(bank) - (12 - i - 1)
            max_v = np.argmax(bank[start:end])
            joltage += str(bank[start+max_v])
            start = start + max_v + 1
        
        acc += int(joltage)
    return acc


def parse_data(data):
    ar = []
    for i, bank in enumerate(data):
        ar.append(np.array([int(bank[c]) for c in range(0, len(bank))]))
    return ar


if __name__ == "__main__":
    data = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111"
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    data = parse_data(data)

    # result = part1(data)
    # assert result == 357, f"{result}"

    result = part2(data)
    assert result == 3121910778619, f"{result}"
