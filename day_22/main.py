import re


def read_input(file: str):
    with open(file) as f:
        monkey_map, notes = f.read().split('\n\n')

        notes = re.findall(r'\d+|\w', notes)
        for i, v in enumerate(notes):
            if v.isnumeric():
                notes[i] = int(v)

        outer_tiles = {'rows': {}, 'columns': {}}
        monkey_map = monkey_map.splitlines()
        dict_mm = {}

        for i_r, row in enumerate(monkey_map, start=1):
            outer_tiles['rows'][i_r] = {}
            for i_c, v in enumerate(row, start=1):
                if i_c not in outer_tiles['columns']:
                    outer_tiles['columns'][i_c] = {}
                if v in ('.', '#'):
                    if 'left' not in outer_tiles['rows'][i_r]:
                        outer_tiles['rows'][i_r]['left'] = i_c
                    if i_c == len(row):
                        outer_tiles['rows'][i_r]['right'] = i_c
                    if 'top' not in outer_tiles['columns'][i_c]:
                        outer_tiles['columns'][i_c]['top'] = i_r
                    try:
                        if monkey_map[i_r][i_c-1] == ' ':
                            outer_tiles['columns'][i_c]['bottom'] = i_r
                    except IndexError:
                        outer_tiles['columns'][i_c]['bottom'] = i_r
                    dict_mm[(i_r, i_c)] = v

        return dict_mm, outer_tiles, notes


def change_direction(orig_dir: tuple[int, int], param: str) -> tuple[int, int]:
    """Tuple bezeichn. Richtung: 1. Wert vertikal (positiv: nach unten), 2. Wert horiz. (posit.: noach rechts)
       (0, 1) -> R -> (1, 0) -> R -> (0, -1) -> R -> (-1, 0) -> R -> (0, 1)
       (0, 1) -> L -> (-1, 0) -> L -> (0, -1) -> L -> (1, 0) -> L -> (0, 1)"""
    transforms_r = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}
    transforms_l = {(0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0), (1, 0): (0, 1)}
    if param == 'R':
        return transforms_r[orig_dir]
    if param == 'L':
        return transforms_l[orig_dir]


def check_opposite(outer_tiles: dict, position: tuple[int, int], facing: tuple[int, int]) -> tuple[int, int]:
    if not facing[0]:
        result = outer_tiles['rows'][position[0]]
        if facing[1] > 0:
            result = result['left']
        else:
            result = result['right']
        tile_pos = (position[0], result)
    else:
        result = outer_tiles['columns'][position[1]]
        if facing[0] > 0:
            result = result['top']
        else:
            result = result['bottom']
        tile_pos = (result, position[1])
    return tile_pos


def move_forward(position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    return position[0] + direction[0], position[1] + direction[1]


def solve(monkey_map: dict[tuple[int, int], str], outer_tiles: dict, notes: list[str | int]):
    value_facing = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}

    facing = (0, 1)
    position = (1, 1)

    for v in notes:
        if v in ('R', 'L'):
            facing = change_direction(facing, v)
        else:
            for step in range(v):
                new_pos = move_forward(position, facing)
                if new_pos not in monkey_map:
                    opposite = check_opposite(outer_tiles, position, facing)
                    if monkey_map[opposite] == '.':
                        position = opposite
                elif monkey_map[new_pos] == '.':
                    position = new_pos
    return 1000 * position[0] + 4 * position[1] + value_facing[facing]


if __name__ == '__main__':
    monkey_map, outer_tiles, notes = read_input('test_input.txt')
    print(monkey_map)
    print(outer_tiles)
    print(notes)
    print(solve(monkey_map, outer_tiles, notes))

