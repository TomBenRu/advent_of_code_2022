from collections import defaultdict
from copy import deepcopy

grid_1 = defaultdict(str)

sand_start = (500, 0)

with open('input.txt', 'r') as f:
    data = [[[int(xy) for xy in c.split(',')] for c in p.strip().split(' -> ')] for p in f.readlines()]

rock_coords = set()

lowest_rock = 0

for i, path in enumerate(data):
    for j, corner in enumerate(path[:-1]):
        if corner[1] > lowest_rock:
            lowest_rock = corner[1]
        c1, c2 = corner, path[j + 1]
        if c1[0] == c2[0]:
            y1, y2 = sorted([c1[1], c2[1]])
            rock_coords |= {(c1[0], cy) for cy in range(y1, y2 + 1)}
        else:
            x1, x2 = sorted([c1[0], c2[0]])
            rock_coords |= {(cx, c1[1]) for cx in range(x1, x2 + 1)}


for point in rock_coords:
    grid_1[point] = '#'

grid_2 = deepcopy(grid_1)


def grain_fall(grain: tuple[int, int]) -> tuple[int, int] | None:
    x, y = grain
    if not part_1:
        if y == lowest_rock + 1:
            return None
    if not grid[new_pos:=(x, y+1)]:
        return new_pos
    else:
        if not grid[new_pos:=(x-1, y+1)]:
            return new_pos
        else:
            if not grid[new_pos:=(x+1, y+1)]:
                return new_pos
            else:
                return None


for part_1 in (True, False):
    leave_simulation = False
    grid = grid_1 if part_1 else grid_2
    while True:
        grain_actual = sand_start
        while True:
            if new_pos := grain_fall(grain_actual):
                grain_actual = new_pos
                if part_1:
                    if grain_actual[1] > lowest_rock:
                        leave_simulation = True
                        break
            else:
                grid[grain_actual] = 'o'
                if not part_1:
                    if grain_actual == sand_start:
                        leave_simulation = True
                break
        if leave_simulation:
            break

fixed_1 = [k for k, v in grid_1.items() if v == 'o']
print('part 1:', len(fixed_1))

fixed_2 = [k for k, v in grid_2.items() if v == 'o']
print('part 2', len(fixed_2))
