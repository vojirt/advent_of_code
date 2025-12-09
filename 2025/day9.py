import numpy as np
import tqdm
from shapely import Polygon

def parse_data(data):
    arr = np.zeros((len(data), 2), dtype=int)
    for i, line in enumerate(data):
        arr[i, :] = np.array([int(s) for s in line.split(",")])
    return arr

def part1(data):
    areas = np.prod(np.abs(data[:, None, :] - data[None, :, :]) + 1, axis=-1)
    return np.max(areas)

def part2(data):
    all_shape = Polygon(data)
    areas = np.triu(np.prod(np.abs(data[:, None, :] - data[None, :, :]) + 1, axis=-1), k=1)
    sorted_idx = np.unravel_index(np.argsort(-areas, axis=None), areas.shape)
    max_area = 1
    for i in tqdm.tqdm(range(0, sorted_idx[0].shape[0])):
        pts = data[[sorted_idx[0][i], sorted_idx[1][i]], :]
        minx = pts[:, 0].min()
        maxx = pts[:, 0].max()
        miny = pts[:, 1].min()
        maxy = pts[:, 1].max()
        rect = Polygon(((minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)))
        if all_shape.contains(rect):
            max_area = areas[sorted_idx[0][i], sorted_idx[1][i]]
            break
    return max_area


if __name__ == "__main__":
    data = [
        "7,1",
        "11,1",
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3"
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    data = parse_data(data)
    # print(data)

    # result = part1(data)
    # assert result == 50, f"{result}"

    result = part2(data)
    assert result == 24, f"{result}"
