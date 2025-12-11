import numpy as np
import tqdm
from joblib import Parallel, delayed

def parse_data(data):
    devices = {}
    for l in data:
        k, con = l.split(': ')
        con = con.split(' ')
        devices[k] = con
    return devices

def part1(devices):
    current_devices = ["you"]
    counter = 0
    while len(current_devices) > 0:
        node = current_devices[-1]
        current_devices = current_devices[:-1]
        for n in devices[node]:
            if n == "out":
                counter += 1
            else:
                current_devices.append(n)
    return counter

def find_all_paths(devices, start, end):
    current_paths = [start]
    counter = 0
    non_reachable = []
    reach = []
    while len(current_paths) > 0:
        path = current_paths.pop()
        last_node = path[-3:]

        if last_node not in reach and last_node not in non_reachable:
            if not reachable(devices, last_node, end):
                non_reachable.append(last_node)
                continue
            else:
                reach.append(last_node)

        if last_node in non_reachable:
            continue

        for conn in devices[last_node]:
            if conn == end:
                counter += 1
                continue

            if conn != "out": 
                current_paths.append(path+conn)
    return counter


def reachable(devices, start, end):
    current_devices = [start]
    visited = []
    while len(current_devices) > 0:
        node = current_devices[-1]
        current_devices = current_devices[:-1]
        if node in visited:
            continue
        visited.append(node)

        for n in devices[node]:
            if n == end:
                return True
            else:
                if n != "out":
                    current_devices.append(n)
    return False

def part2(devices):

    r1 = find_all_paths(devices, start="svr", end="fft")
    r2 = find_all_paths(devices, start="fft", end="dac")
    assert find_all_paths(devices, start="dac", end="fft") == 0
    r3 = find_all_paths(devices, start="dac", end="out")
    
    return r1*r2*r3

if __name__ == "__main__":
    data = [
        "aaa: you hhh",
        "you: bbb ccc",
        "bbb: ddd eee",
        "ccc: ddd eee fff",
        "ddd: ggg",
        "eee: out",
        "fff: out",
        "ggg: out",
        "hhh: ccc fff iii",
        "iii: out"
    ]
    data = [
        "svr: aaa bbb",
        "aaa: fft",
        "fft: ccc",
        "bbb: tty",
        "tty: ccc",
        "ccc: ddd eee",
        "ddd: hub",
        "hub: fff",
        "eee: dac",
        "dac: fff",
        "fff: ggg hhh",
        "ggg: out",
        "hhh: out"
    ]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    devices = parse_data(data)
    # print(devices)

    # result = part1(devices)
    # assert result == 5, f"{result}"

    result = part2(devices)
    assert result == 2, f"{result}"
