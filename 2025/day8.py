import numpy as np
import tqdm
from functools import reduce

def parse_data(data):
    arr = np.zeros((len(data), 3))
    for i, line in enumerate(data):
        arr[i, :] = np.array([float(s) for s in line.split(",")])
    return arr

def part1(data, num_of_connections = 1000):
    boxes = [[i] for i in range(0, data.shape[0])]

    dists_sq = np.sum(np.pow((data[:, None, :] - data[None, :, :]), 2), axis=-1)
    dists_sorted = np.triu(dists_sq).flatten()
    dists_sorted = np.sort(dists_sorted[dists_sorted > 0])
    
    counter = -1 
    tbar = tqdm.tqdm(range(0, num_of_connections))
    for _ in tbar:
        tbar.set_description(f"real connections {counter}")
        boxes_closest = np.zeros(len(boxes), dtype=int)
        boxes_closest_dist = np.zeros(len(boxes), dtype=float)
        for i, b in enumerate(boxes):
            not_box = list(reduce(lambda x, y: x + y, [boxes[j] for j in range(0, len(boxes)) if j != i], []))
            if len(b) > 1:
                mindist_to_any = np.min(dists_sq[b, :][:, not_box], axis=0)  
            else:
                mindist_to_any = dists_sq[b, not_box]
            min_idd = np.argmin(mindist_to_any)
            boxes_closest[i] = [j for j in range(0, len(boxes)) if not_box[min_idd] in boxes[j]][0]
            boxes_closest_dist[i] = mindist_to_any[min_idd]
       
        closest = np.argmin(boxes_closest_dist)
        new_box = [] + boxes[closest] + boxes[boxes_closest[closest]]

        counter += 1
        while boxes_closest_dist[closest] != dists_sorted[counter] and counter <= num_of_connections:
            counter += 1

        if counter >= num_of_connections:
            break

        boxes = [boxes[i] for i in range(0, len(boxes)) if i != closest and i != boxes_closest[closest]] + [new_box]
    sizes = [len(boxes[b]) for b in range(0, len(boxes))]
    return np.prod(np.sort(sizes)[-3:])

def part2(data):
    boxes = [[i] for i in range(0, data.shape[0])]

    dists_sq = np.sum(np.pow((data[:, None, :] - data[None, :, :]), 2), axis=-1)
    last_connection = (-1, -1)
    while True:
        boxes_closest = np.zeros(len(boxes), dtype=int)
        boxes_closest_dist = np.zeros(len(boxes), dtype=float)
        boxes_connections = []
        for i, b in enumerate(boxes):
            not_box = list(reduce(lambda x, y: x + y, [boxes[j] for j in range(0, len(boxes)) if j != i], []))
            if len(b) > 1:
                pdist = dists_sq[b, :][:, not_box]
            else:
                pdist = dists_sq[b, not_box][None, :]
            min_idd = np.unravel_index(np.argmin(pdist, axis=None), pdist.shape)
            boxes_closest[i] = [j for j in range(0, len(boxes)) if not_box[min_idd[1]] in boxes[j]][0]
            boxes_closest_dist[i] = pdist[min_idd]
            boxes_connections.append((data[b[min_idd[0]], :], data[not_box[min_idd[1]]]))
            
        closest = np.argmin(boxes_closest_dist)
        new_box = [] + boxes[closest] + boxes[boxes_closest[closest]]

        boxes = [boxes[i] for i in range(0, len(boxes)) if i != closest and i != boxes_closest[closest]] + [new_box]
        if len(boxes) == 1:
            last_connection = boxes_connections[closest]
            break
        print(len(boxes))

    return last_connection[0][0]*last_connection[1][0]


if __name__ == "__main__":
    data = [
    "162,817,812", 
    "57,618,57", 
    "906,360,560", 
    "592,479,940", 
    "352,342,300", 
    "466,668,158", 
    "542,29,236", 
    "431,825,988", 
    "739,650,466", 
    "52,470,668", 
    "216,146,977", 
    "819,987,18", 
    "117,168,530", 
    "805,96,715", 
    "346,949,466", 
    "970,615,88", 
    "941,993,340", 
    "862,61,35", 
    "984,92,344", 
    "425,690,689"]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    data = parse_data(data)
    # print(data)

    # result = part1(data, num_of_connections=1000)
    # assert result == 40, f"{result}"

    result = part2(data)
    assert result == 25272, f"{result}"
