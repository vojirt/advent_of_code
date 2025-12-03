import numpy as np

if __name__ == "__main__":
    lines = []
    with open('data1.txt') as f:
        for line in f:
            l = line.rstrip('\n')
            lines.append(int(l[1:]) * (1 if l[0] == 'R' else -1))

    # lines = [ -68, -30, 48, -5, 60, -55, -1, -99, 14, -82 ]
    # print(lines)

    c_d = 50
    counter = 0
    for d in lines:
        abs_d = np.abs(d)
        full_rot = abs_d // 100
        partiall_rot = abs_d % 100
         
        counter += full_rot

        c_d_tmp = c_d + np.sign(d) * partiall_rot

        if c_d != 0 and (c_d_tmp <= 0 or c_d_tmp >= 100) and (partiall_rot > 0 or full_rot == 0):
            counter += 1
        c_d = c_d_tmp % 100

    # NOTE: part 1 was lost in translation :) but I faintly remember using % and some additions
    print(counter)
