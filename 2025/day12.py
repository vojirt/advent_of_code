import numpy as np


def parse_data(data):
    shapes = {} 
    sep = np.nonzero([1 if l == "" else 0 for l in data])[0]
    for i in range(0, sep.shape[0]):
        if i == 0:
            shape = data[:sep[i]]
        else:
            shape = data[sep[i-1] + 1:sep[i]]

        shape_id = int(shape[0].split(':')[0])
        shape = np.array([list(l) for l in shape[1:]])
        shape[shape=="#"] = 1
        shape[shape=="."] = 0
        shapes[shape_id] = shape.astype(int)

    trees = [] 
    for l in data[sep[-1]+1:]:
        size, counts = l.split(": ")
        size = [int(s) for s in size.split('x')]
        counts = {i:int(c) for i, c in enumerate(counts.split(' ')) if int(c) > 0}
        trees.append([size[::-1], counts])

    return shapes, trees

def part1(shapes, trees):
    pass

def part2(shapes, trees):
    pass


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

    # result = part2(shapes, trees)
    # assert result == 2, f"{result}"
