import string
import pprint
from collections import deque
from typing import Self

char2int = {c: i for i, c in enumerate(string.ascii_lowercase)}


def parse_data(file: str = 'test_input.txt') -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    with open(file, 'r') as f:
        area = [list(row.strip()) for row in f.readlines()]

    start = None
    goal = None

    for i_row, row in enumerate(area):
        for i_col, col in enumerate(row):
            if col == 'S':
                start = (i_row + 1, i_col + 1)
                area[i_row][i_col] = 0
            elif col == 'E':
                goal = (i_row + 1, i_col + 1)
                area[i_row][i_col] = 25
            else:
                area[i_row][i_col] = char2int[col]

    for row in area:
        row.insert(0, 99)
        row.append(99)

    area.insert(0, [99] * len(area[0]))
    area.append([99] * len(area[0]))

    print(f'{start = }, {goal = }')
    pprint.pprint(area)

    return area, start, goal


class Location:
    def __init__(self, loc: tuple[int, int], distance_from_start: float, level: int, neigbours: set[tuple[int, int]] = None):
        self.loc = loc
        self.level = level
        self.distance_from_start: float = distance_from_start
        if neigbours is None:
            self.neighbours: set[tuple[int, int]] = set()
        else:
            self.neighbours: set[tuple[int, int]] = neigbours

    def __repr__(self):
        return f'{self.__class__.__name__}({self.loc = }, {self.level = }, {self.neighbours = })'


def neighbours_coords(location: tuple[int, int]) -> list[tuple[int, int]]:
    return [l for l in [(location[0], location[1] - 1), (location[0], location[1] + 1),
            (location[0] - 1, location[1]), (location[0] + 1, location[1])]
            if area[l[0]][l[1]] - area[location[0]][location[1]] <= 1]


def solve(curr_coord: tuple[int, int]) -> list[tuple[int, int]] | None:
    print(f'{curr_coord = }')
    dist_neighbours = all_locations[curr_coord].distance_from_start + 1
    if not all_locations[curr_coord].neighbours:
        return
    num_turns = len(all_locations[curr_coord].neighbours)
    result = None
    len_result = float('inf')
    for n in all_locations[curr_coord].neighbours:
        print(f'{n = }')
        if n == goal:
            if all_locations[goal].distance_from_start <= dist_neighbours:
                num_turns -= 1
                continue
            else:
                all_locations[goal].distance_from_start = dist_neighbours
                return [n]
        elif all_locations[n].distance_from_start <= dist_neighbours:
            num_turns -= 1
            continue
        else:
            all_locations[n].distance_from_start = dist_neighbours
            next_loc = solve(n)
            # print(f'{next_loc = }')
            if not next_loc:
                num_turns -= 1
                continue
            elif (len_loc := len(next_loc)) < len_result:
                result = next_loc
                print(f'{result = }')
                len_result = len_loc
                num_turns -= 1
            else:
                num_turns -= 1
                continue
    while num_turns:
        print(f'in der Schleife {curr_coord}')
        pass
    return result + [curr_coord] if result else None


if __name__ == '__main__':
    area, start, goal = parse_data()
    all_locations: dict[tuple, Location] = {(i_row, i_col): Location((i_row, i_col), float('inf'), col)
                                            for i_row, row in enumerate(area)
                                            for i_col, col in enumerate(row) if col != 99}
    for coord, loc in all_locations.items():
        neigbours = neighbours_coords(coord)
        loc.neighbours = neigbours
    all_locations[start].distance_from_start = 0

    res = solve(curr_coord=start)[::-1]
    print(f'{res = }, {len(res) = }')
