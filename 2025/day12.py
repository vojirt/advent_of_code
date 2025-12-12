import numpy as np
from scipy.signal import convolve2d
import cv2

def parse_data(data):
    shapes = {} 
    sep = np.nonzero([1 if l == "" else 0 for l in data])[0]
    for i in range(0, sep.shape[0]):
        if i == 0:
            shape = data[:sep[i]]
        else:
            shape = data[sep[i-1] + 1:sep[i]]

        shape_id = int(shape[0].split(':')[0])
        shape = np.array([list(l.replace('#', '1').replace('.', '0')) for l in shape[1:]], dtype=int)
        shape[shape==0] = 1000    # some large value that does not overlap with the maximum fill size of the same (e.g. 3x3 shape -> max 9 filled values, thus 10 would be enough in that case) 
        shape_all = []
        # generate all posible orientations of the shape
        for flip_lr in range(2):
            for flip_ud in range(2):
                for rot in range(4):
                    new_shape = shape.copy()
                    if flip_lr == 1:
                        new_shape = np.fliplr(new_shape)
                    if flip_ud == 1:
                        new_shape = np.flipud(new_shape)
                    if rot > 0:
                        new_shape = np.rot90(new_shape, rot)
                    shape_all.append(new_shape)
        # only uniques shape orientations
        shapes[shape_id] = np.unique(np.array(shape_all), axis=0)
    trees = [] 
    for l in data[sep[-1]+1:]:
        size, counts = l.split(": ")
        size = [int(s) for s in size.split('x')]
        counts = {i:int(c) for i, c in enumerate(counts.split(' ')) if int(c) > 0}
        trees.append([size[::-1], counts])

    return shapes, trees

def rank_placements_of_shape(tree2d, shape_list):
    placements = []
    for shape_id, shape in enumerate(shape_list):
        out = convolve2d(tree2d, np.fliplr(np.flipud(shape)), mode='same', boundary='fill', fillvalue=1)    # for some reason the kernel needs to be flipped horizontally and vertically
        score =  out // 1000 # ... how many of empty spaces of the shape were filled at that location, used for scoring (higher the number -> higher "compactness")
        valid =  (out % 1000) == 0 #... if it overlaps any already placed shape in tree2d
        valid_idx = np.nonzero(valid)
        for i in range(0, valid_idx[0].shape[0]):
            r = valid_idx[0][i]
            c = valid_idx[1][i]
            placements.append([shape_id, r, c, score[r, c]])
    placements = np.array(placements, dtype=int)
    if len(placements) > 1:
        placements = placements[np.argsort(placements[:, -1])[::-1], :]
    return placements

def place_shape(tree2d, shape, r, c):
    assert shape.shape[0] == 3 and shape.shape[1] == 3, "Assumes only 3x3 shapes"
    idx = np.nonzero(shape == 1)
    idx_r = r+idx[0]-1
    idx_c = c+idx[1]-1
    tree2d[idx_r, idx_c] = 1
    return idx_r, idx_c

def part1(shapes, trees):
    tree2d = np.zeros((5,5))
    print(shapes[0][[0, 6], ...])
    out = rank_placements_of_shape(tree2d, shapes[0][[0,6], ...])
    place_shape(tree2d, shapes[0][[0, 6], ...][out[0, 0], ...], out[0, 1], out[0, 2])
    print(out)
    print(tree2d)
    print("=================")
    out = rank_placements_of_shape(tree2d, shapes[0][[0,6], ...])
    place_shape(tree2d, shapes[0][[0, 6], ...][out[0, 0], ...], out[0, 1], out[0, 2])
    print(out)
    print(tree2d)
    print("=================")
    out = rank_placements_of_shape(tree2d, shapes[0][[0,6], ...])
    print(out)
    
    return 0


if __name__ == "__main__":
    data = [
     "0:",
     "###",
     "##.",
     "##.",
     "",
     "1:",
     "###",
     "##.",
     ".##",
     "",
     "2:",
     ".##",
     "###",
     "##.",
     "",
     "3:",
     "##.",
     "###",
     "##.",
     "",
     "4:",
     "###",
     "#..",
     "###",
     "",
     "5:",
     "###",
     ".#.",
     "###",
     "",
     "4x4: 0 0 0 0 2 0",
     "12x5: 1 0 1 0 2 2",
     "12x5: 1 0 1 0 3 2"
    ]

    # data = [] 
    # with open("data.txt") as fobj:
    #     for line in fobj:
    #         data.append(line.rstrip('\n'))

    shapes, trees = parse_data(data)
    # print(shapes, trees)

    result = part1(shapes, trees)
    assert result == 2, f"{result}"
