import torch

def parse_data(data):
    int_data = []
    for line in data:
        int_data.append([0 if line[c]=='.' else 1 for c in range(0, len(line))])
    return torch.tensor(int_data, dtype=float)

def part1(data: torch.Tensor):
    avg_data = torch.nn.functional.avg_pool2d(data[None, None, ...], kernel_size=3, stride=1, padding=1)[0, 0, ...]
    return int(((avg_data <= 4.0/9.0) * data).sum().item())

def part2(data: torch.Tensor):
    removed = 0
    for i in range(0, data.shape[0]*data.shape[1]):
        avg_data = torch.nn.functional.avg_pool2d(data[None, None, ...], kernel_size=3, stride=1, padding=1)[0, 0, ...]
        to_be_removed = (avg_data <= 4.0/9.0) * data
        to_be_removed_count = int(to_be_removed.sum().item()) 
        if to_be_removed_count == 0:
            break
        removed += to_be_removed_count 
        data[to_be_removed.long() == 1] = 0
    return removed

if __name__ == "__main__":
    data = ["..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@."]

    data = [] 
    with open("data.txt") as fobj:
        for line in fobj:
            data.append(line.rstrip('\n'))

    data = parse_data(data)
    
    # result = part1(data)
    # assert result == 13, f"{result}"

    result = part2(data)
    assert result == 43, f"{result}"
