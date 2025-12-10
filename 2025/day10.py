import numpy as np
import tqdm
from scipy.optimize import linprog

def parse_data(data):
    lights, buttons, joltage = [], [], []
    
    def parse_buttons(buttons):
        b_int = 0
        for b in buttons:
            b_int |= 1 << int(b)
        return b_int 

    for line in data:
        l = line.split(' ')
        lights.append(int("".join(['0' if c=='.' else '1' for c in l[0][1:-1]][::-1]), 2))
        buttons.append(np.array([parse_buttons(buttons[1:-1].split(',')) for buttons in l[1:-1]], dtype=int))
        joltage.append(np.array([int(j) for j in l[-1][1:-1].split(',')], dtype=int))
    return lights, buttons, joltage

def process_circuit(lights, buttons):
    possibilities = buttons.copy() 
    if np.any(possibilities == lights):
        return 1 

    for level in range(1, 100000):
        idx = np.triu_indices(n=buttons.shape[0], m=possibilities.shape[0])
        possibilities = (buttons[:, None] ^ possibilities[None, :])[idx]
        if np.any(possibilities == lights):
            break

    return level + 1

def part1(lights, buttons):
    press = 0
    for i in range(0, len(lights)):
        press += process_circuit(lights[i], buttons[i])
    return press

def process_circuit_joltage(joltage, buttons):
    button_idx_repr = np.array([np.frombuffer(np.binary_repr(s, width=joltage.shape[0]).encode("ascii"), dtype="u1")[::-1]-48 for s in buttons]).astype(int)
    c = np.ones(buttons.shape[0])
    A_eq = button_idx_repr.T
    
    # MAKES NO FUCKING DIFFERENCE
    # bounds_up = joltage[None, :] * button_idx_repr
    # bounds_up[bounds_up == 0] = bounds_up.max()
    # bounds_up = np.min(bounds_up, axis=-1)
    #
    # bounds_l = np.zeros_like(c)
    # mask = button_idx_repr.sum(axis=0) == 1
    # if mask.sum() > 0:
    #     for idd in np.nonzero(mask)[0]:
    #         button_mask = button_idx_repr[:, idd] == 1
    #         bounds_l[button_mask] = joltage[idd] 
    # bounds = np.stack([bounds_l, bounds_up], axis=1)
    
    success = False
    for i in range(0, 1000):
        res = linprog(c=c, A_eq=A_eq, b_eq=joltage, method="highs", integrality=np.ones(buttons.shape[0], dtype=int), 
                      options = {"presolve":True, "primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10, "random_seed": i}) 
        if ((button_idx_repr * res.x.astype(int)[:, None]).sum(axis=0) - joltage).sum() != 0 and res.status != 0:
            assert False, "blabla"
        if ((button_idx_repr * res.x.astype(int)[:, None]).sum(axis=0) - joltage).sum() == 0:
            success = True
            break
    if not success:
        print("AAAAAAAHHHH, fuck of with suboptimal solution you cheating bastard")
    return res.x.astype(int).sum()

def part2(buttons, joltage):
    press = 0
    for i in tqdm.tqdm(range(0, len(joltage))):
        press += process_circuit_joltage(joltage[i], buttons[i]) 
    return press

if __name__ == "__main__":
    data = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    lights, buttons, joltage = parse_data(data)
    # print(lights, buttons, joltage)

    # result = part1(lights, buttons)
    # assert result == 7, f"{result}"

    result = part2(buttons, joltage)
    assert result == 33, f"{result}"
