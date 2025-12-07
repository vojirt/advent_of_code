import numpy as np


def parse_data(data):
    data = np.array(data, dtype=bytes)
    return data.view('S1').reshape((data.size, -1))

def part1(data):
    beams = np.nonzero(data[0, :] == b'S')[0]
    acc = 0
    for row in range(1, data.shape[0]):
        splitters = np.nonzero(data[row, beams] == b'^')[0]
        if splitters.shape[0] == 0:
            continue
        splitters = beams[splitters]
        acc += splitters.shape[0] 

        beams = np.setdiff1d(beams, splitters)
        beams = np.union1d(beams, splitters-1)
        beams = np.union1d(beams, splitters+1)

    return acc

def part2(data):
    beams = np.nonzero(data[0, :] == b'S')[0]
    counters = np.zeros_like(data, dtype=int)
    counters[0, beams[0]] = 1
    for row in range(1, data.shape[0]):
        counters[row, :] = counters[row-1, :]
        splitters = np.nonzero(data[row, beams] == b'^')[0]
        if splitters.shape[0] == 0:
            continue

        splitters = beams[splitters]
        s_p = splitters + 1 
        s_m = splitters - 1 
        counters[row, s_p] += counters[row, splitters] 
        counters[row, s_m] += counters[row, splitters] 
        counters[row, splitters] = 0

        beams = np.setdiff1d(beams, splitters)
        beams = np.union1d(beams, splitters-1)
        beams = np.union1d(beams, splitters+1)
    return counters[-1, :].sum()

if __name__ == "__main__":
    data = [
".......S.......",
"...............",
".......^.......",
"...............",
"......^.^......",
"...............",
".....^.^.^.....",
"...............",
"....^.^...^....",
"...............",
"...^.^...^.^...",
"...............",
"..^...^.....^..",
"...............",
".^.^.^.^.^...^.",
"..............."
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    data = parse_data(data)
    # print(data)

    # print(ranges, ingredients)

    # result = part1(data)
    # assert result == 21, f"{result}"

    result = part2(data)
    assert result == 40, f"{result}"
