import numpy as np


def parse_data(data):
    data_np = np.array(data)
    idd = np.where(data_np == "")[0][0]
    ranges = data_np[:idd] 
    ranges = np.array([np.array(ranges[i].split("-")).astype(int) for i in range(0, ranges.shape[0])])
    ingredients = data_np[idd+1:].astype(int)
    return ranges, ingredients

def part1(ranges, ingredients):
    inrange = (ingredients[:, None] - ranges[None, :, 0]) / (ranges[None, :, 1] - ranges[None, :, 0] + 0.1)
    inrange = np.any((inrange >= 0) * (inrange <= 1), axis=-1).sum()
    return inrange

def part2(ranges, ingredients):
    ranges = ranges[np.argsort(ranges[:, 0]), :]
    
    for i in range(0, ranges.shape[0]):
        if (ranges[i, 1] - ranges[i, 0]) < 0:
            continue
        inrange_start = (ranges[i+1:, 0] - ranges[i, 0]) / (ranges[i, 1] - ranges[i, 0] + 0.1)
        inrange_start = ((inrange_start >= 0) * (inrange_start <= 1))
        ranges[np.nonzero(inrange_start)[0]+i+1, 0] = ranges[i, 1] + 1

    ranges_size = (ranges[:, 1] - ranges[:, 0] + 1)
    return (ranges_size[ranges_size > 0]).sum()

if __name__ == "__main__":
    data = [
            "3-5",
            "10-14",
            "16-20",
            "12-18",
            "",
            "1",
            "5",
            "8",
            "11",
            "17",
            "32"
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    # print(data)
    ranges, ingredients = parse_data(data)

    # print(ranges, ingredients)

    # result = part1(ranges, ingredients)
    # assert result == 3, f"{result}"

    result = part2(ranges, ingredients)
    # assert result == 14, f"{result}"
    assert result == 354149806372909, f"{result}"

