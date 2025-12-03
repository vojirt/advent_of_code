import numpy as np

def load_data():
    def parse_data(data):
        ds = data.split(',')
        return [[int(d.split('-')[0]), int(d.split('-')[1])] for d in ds] 

    # return parse_data("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124")
    with open("data.txt") as fobj:
        return parse_data(fobj.readline())
    

def check_pattern(s, part2_flag):
    si = np.array([int(s[c]) for c in range(0, len(s))])
    ids = np.where(si == si[0])[0]

    if ids.shape[0] <= 1:
        return -1,-1

    # for i in range(1, ids.shape[0]):
    for i in range(ids.shape[0]-1, 0, -1):      # to always find the largest first => allow skipping
        found_pattern = True
        
        pattern_length = (ids[i]-ids[0]) 
        ids_p = ids[np.where(np.mod(ids, pattern_length) == 0)]

        if not part2_flag and pattern_length != si.shape[0] // 2:
            continue

        if not part2_flag and pattern_length == 1 and si.shape[0] % 2 != 0:
            continue

        if pattern_length*ids_p.shape[0] != si.shape[0]:
            continue

        if ids_p[-1] + pattern_length != si.shape[0]:
            continue

        if pattern_length == 1 and ids_p.shape[0] != si.shape[0]:
            continue

        found_pattern_tmp = True
        for off in range(1, ids_p[1]):
            if not np.all(si[ids_p+off] == si[ids_p[0]+off]):
                found_pattern_tmp = False
                break

        found_pattern &= found_pattern_tmp

        if found_pattern:
            return pattern_length, si.shape[0]

    return -1,-1


def run(part2_flag=False):
    data = load_data()
    
    acc = 0
    for d in data:
        for i in range(d[0], d[1]+1):
            pattern, size = check_pattern(str(i), part2_flag)
            if pattern > 0:
                # print(f"found pattern in {i} of length {pattern}")
                acc += i
                # this may not be always correct? if there exist pattern of multiple lengts and the longest is not returned.
                i+= 10**(size-pattern)
    return acc


if __name__ == "__main__":
    # result = run()
    # assert result == 1227775554, f"{result}"

    # NOTE: the code was hacked and hacked so no guarantee it will work correctly for part 1 :)
    result = run(True)
    assert result == 4174379265, f"{result}"


