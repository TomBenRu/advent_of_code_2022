import pprint

with open('input.txt') as f:
    data: list[tuple[int, int, int]] = [tuple(int(c) for c in droplet.split(',')) for droplet in f.read().splitlines()]


num_contacts = 0

open_sides = [[(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
              for x, y, z in data]

open_sides = [s for d in open_sides for s in d]

for droplet in data:
    for droplet_2 in data:
        if droplet == droplet_2:
            continue
        if droplet[0] == droplet_2[0] and droplet[1] == droplet_2[1] and abs(droplet[2] - droplet_2[2]) == 1:
            if droplet in open_sides:
                open_sides.remove(droplet)
            if droplet_2 in open_sides:
                open_sides.remove(droplet_2)
            num_contacts += 1
        if droplet[0] == droplet_2[0] and droplet[2] == droplet_2[2] and abs(droplet[1] - droplet_2[1]) == 1:
            num_contacts += 1
            if droplet in open_sides:
                open_sides.remove(droplet)
            if droplet_2 in open_sides:
                open_sides.remove(droplet_2)
        if droplet[1] == droplet_2[1] and droplet[2] == droplet_2[2] and abs(droplet[0] - droplet_2[0]) == 1:
            num_contacts += 1
            if droplet in open_sides:
                open_sides.remove(droplet)
            if droplet_2 in open_sides:
                open_sides.remove(droplet_2)

print('part_1:', len(data) * 6 - num_contacts)

max_x = max(x for x, _, _ in data)
min_x = min(x for x, _, _ in data)
max_y = max(y for _, y, _ in data)
min_y = min(y for _, y, _ in data)
max_z = max(z for _, _, z in data)
min_z = min(z for _, _, z in data)

print(max_x, min_x, max_y, min_y, max_z, min_z)

print(len(open_sides))


def neighbours(coord: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    x, y, z = coord
    neigb = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
    return neigb


def find_way_out(coord: tuple[int, int, int]) -> bool:
    paths, path_idx, visited = [[coord]], 0, [coord]

    while path_idx < len(paths):
        droplet = paths[path_idx][-1]
        for neighbour in neighbours(droplet):
            # print(f'{neighbour=}')
            if (-1 in neighbour) or neighbour[0] > max_x or neighbour[1] > max_y or neighbour[2] > max_z:
                return True
            if (neighbour in data) or (neighbour in visited):
                continue
            paths.append(paths[path_idx][:] + [neighbour])
            visited.append(neighbour)
        path_idx += 1
    return False


outer_opensites = 0
for i, os in enumerate(open_sides):
    if find_way_out(os):
        outer_opensites += 1
    if not i % 100:
        print(f'{i} sides checked.')

print('part 2:', outer_opensites)


