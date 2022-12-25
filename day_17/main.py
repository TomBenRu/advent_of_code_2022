

with open('input.txt') as f:
    jet_pattern = f.read()

with open('rocks.txt') as f:
    rocks = [[point
              for line in [[(x, y) for x, p in enumerate(list(li)) if p == '#']
                           for y, li in enumerate(r.splitlines()[::-1])]
              for point in line] for r in f.read().split('\n\n')]
    print(rocks)


def calculate_start(rock_pattern: list[tuple[int, int]], topline: list[tuple[int, int]]) -> list[tuple[int, int]]:
    highest_rock = max(y for _, y in topline)
    rock = [(x+3, y+highest_rock+4) for x, y in rock_pattern]
    return rock


def fall(rock: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_positions = [(x, y-1) for x, y in rock]
    return new_positions


def push(rock: list[tuple[int, int]], direction: int) -> list[tuple[int, int]]:
    new_position = [(x+direction, y) for x, y in rock]
    return new_position


def most_left(rock: list[tuple[int, int]]) -> int:
    min_x = min([x for x, _ in rock])
    return min_x


def most_right(rock: list[tuple[int, int]]) -> int:
    max_x = max([x for x, _ in rock])
    return max_x


def collision(rock: list[tuple[int, int]], topline: list[tuple[int, int]]) -> bool:
    collided = bool(set(rock) & set(topline))
    return collided


def calclulate_new_topline(rock: list[tuple[int, int]], topline: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return rock + topline


def print_rock(rock):
    max_y = max(y for _, y in rock)
    min_y = min(y for _, y in rock)
    grid = [['-' if row == 0 else '|' if col in (0, 8) else '.' for col in range(9)] for row in range(max([min_y, max_y-24]), max_y + 1)]
    for r_x, r_y in rock:
        if r_y-max([min_y, max_y-24]) < 0:
            continue
        try:
            grid[r_y-max([min_y, max_y-24])][r_x] = '@'
        except:
            pass
    for line in grid[::-1]:
        print(''.join(line))


def solve(num_stones: int):
    topline = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
    height_after_begin = 0
    height_1_jetloop = 0
    height_end = 0
    num_stones_begin = 0
    num_stones_1_jetloop = 0
    height_between = 0
    num_stones_end = 0
    height_befor_final = 0
    num_stones_before_final = 0
    jet_idx = 0
    for idx in range(num_stones):
        rock_idx = idx % 5
        rock = calculate_start(rocks[rock_idx], topline)
        # print_rock(rock + topline)
        # print()
        #input()
        while True:
            # print(rock)
            # print(jet_idx)
            direction = 1 if jet_pattern[jet_idx] == '>' else -1
            if (direction == 1 and most_right(rock) < 7) or (direction == -1 and most_left(rock) > 1):
                pushed_rock = push(rock[:], direction)
                if not collision(pushed_rock, topline):
                    rock = pushed_rock
            jet_idx = 0 if jet_idx == len(jet_pattern) - 1 else jet_idx + 1
            if height_befor_final:
                if jet_idx == 0:
                    topline = [(x, y) for x, y in topline if y > (max(yy for _, yy in topline) - 26)]
                    # print_rock(topline)
                    # input()
                if idx == num_stones_before_final + num_stones_end:
                    height_end = max({y for _, y in topline}) - height_befor_final
                    height_after_all = height_after_begin + height_between + height_end
                    return height_after_all

            if jet_idx == 0:
                if num_stones_begin and num_stones_1_jetloop and height_after_begin and height_1_jetloop:
                    height_between = height_1_jetloop * ((num_stones - num_stones_begin) // num_stones_1_jetloop)
                    num_stones_end = (num_stones - num_stones_begin) % num_stones_1_jetloop
                    num_stones_before_final = idx
                    height_befor_final = max({y for _, y in topline})
                else:
                    num_stones_1_jetloop = idx - num_stones_begin if (num_stones_1_jetloop == 0 and num_stones_begin) else 0
                    num_stones_begin = idx if num_stones_begin == 0 else num_stones_begin
                    height_1_jetloop = max({y for _, y in topline}) - height_after_begin if (not height_1_jetloop and height_after_begin) else 0
                    height_after_begin = max({y for _, y in topline}) if height_after_begin == 0 else height_after_begin
                    # print_rock(topline)
                    # print(idx, len(jet_pattern))
                    # print(f'{num_stones_begin=}, {num_stones_1_jetloop=}, {height_after_begin=}, {height_1_jetloop=}')
                    topline = [(x, y) for x, y in topline if y > (max(yy for _, yy in topline) - 26)]
                    # print_rock(topline)
                    # input()

            fallen_rock = fall(rock[:])
            if collision(fallen_rock, topline):
                topline = calclulate_new_topline(rock, topline)
                break
            else:
                rock = fallen_rock
    return topline


if __name__ == '__main__':
    num_stones_1 = 2022
    num_stones_2 = 1_000_000_000_000
    print('part 1:', max((y for _, y in solve(num_stones_1))))
    print('part 2:', solve(num_stones_2))
