from copy import deepcopy


def get_data(file: str):
    with open(file) as f:
        data = {i: [i, v] for i, v in enumerate(list(map(int, f.read().splitlines())))}
    return data


def rearange_numbers_to_list(numbers: dict[int, list[int, int]]) -> list[int]:
    return [v[1] for v in sorted(numbers.values(), key=lambda x: x[0])]


def move_number(numbers: dict[int, list[int, int]], orig_id: int) -> dict[int, list[int, int]]:
    to_move = numbers[orig_id]
    act_pos, move = to_move.copy()

    move = move % (len(numbers) - 1)

    while move < 0:
        move = len(numbers) - 1 + move
    if move % (len(numbers) - 1) == 0:
        return numbers

    move = move % (len(numbers) - 1)

    new_pos = (act_pos - (len(numbers) - 1) + move) if (act_pos + move) > (len(numbers) - 1) else act_pos + move

    if new_pos == 0:
        new_pos = 6
    if new_pos < act_pos:
        # positionen aller zahlen mit act_pos > pos >= new_pos werden um 1 erhöht.
        for i, n in numbers.items():
            if i == orig_id:
                continue
            if act_pos > n[0] >= new_pos:
                n[0] += 1
    if new_pos > act_pos:
        # positionen aller Zahlen mit act_pos < pos <= new_pos werden um 1 ernniedrigt.
        for i, n in numbers.items():
            if i == orig_id:
                continue
            if act_pos < n[0] <= new_pos:
                n[0] -= 1
    numbers[orig_id][0] = new_pos
    return numbers


def solve(numbers: dict[int, list[int, int]]) -> tuple[int, dict[int, list[int, int]]]:
    for i in range(len(numbers)):
        numbers = move_number(numbers, i)
        # print(rearange_numbers_to_list(numbers))
        # input()
    result_list = rearange_numbers_to_list(numbers)
    index_val_0 = result_list.index(0)
    searched_nums = (result_list[(1000 + index_val_0) % len(numbers)],
                     result_list[(2000 + index_val_0) % len(numbers)],
                     result_list[(3000 + index_val_0) % len(numbers)])
    result = sum(searched_nums)
    return result, numbers


if __name__ == '__main__':
    data = get_data('input.txt')
    numbers = deepcopy(data)
    result, _ = solve(numbers)
    print('part 1:', result)

    # part 2
    decryption_key = 811589153
    numbers = deepcopy(data)
    for i in numbers:
        numbers[i][1] *= decryption_key

    for i in range(10):
        res, numbers = solve(numbers)

    print('part 2', res)

