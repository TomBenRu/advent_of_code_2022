import re


with open('input.txt', 'r') as f:
    data = [re.findall(r'-*\d+', l.strip()) for l in f.readlines()]
    data = [[(int(l[0]), int(l[1])), (int(l[2]), int(l[3]))] for l in data]

all_sensors_and_beacons = {p for pair in data for p in pair}
no_beacons = set()
# curr_row = 10
curr_row = 2_000_000
max_xy__distress_signal = 4_000_000  # test_input: 20

not_poss_in_row = set()

for (s_x, s_y), (b_x, b_y) in data:
    manh_dist = abs(s_x - b_x) + abs(s_y - b_y)
    if (dist_in_curr_row := (manh_dist - abs(s_y - curr_row))) < 0:
        continue
    p_in_manh_dist_in_row = set((x, curr_row) for x in range(s_x - dist_in_curr_row, s_x + dist_in_curr_row + 1))
    not_poss_in_row |= p_in_manh_dist_in_row

print('part 1:', len(not_poss_in_row-all_sensors_and_beacons))

for row in range(max_xy__distress_signal + 1):
    if not row % 100_000:
        print(f'check row {row}')
    x_coords = [(0, max_xy__distress_signal+1)]
    for (s_x, s_y), (b_x, b_y) in data:
        manh_dist = abs(s_x - b_x) + abs(s_y - b_y)
        if (dist_in_curr_row := (manh_dist - abs(s_y - row))) < 0:
            continue
        x_low, x_high = max(0, s_x - dist_in_curr_row), s_x + dist_in_curr_row + 1
        new_x_coords = []
        for part_low, part_high in x_coords:
            if part_low <= x_low <= part_high and part_low <= x_high <= part_high:
                if x_low - part_low:
                    new_x_coords.append((part_low, x_low))
                if part_high - x_high:
                    new_x_coords.append((x_high, part_high))
            elif part_low <= x_low <= part_high:
                if x_low - part_low:
                    new_x_coords.append((part_low, x_low))
            elif part_low <= x_high <= part_high:
                if part_high - x_high:
                    new_x_coords.append((x_high, part_high))
            elif x_high < part_low or x_low > part_high :
                new_x_coords.append((part_low, part_high))
            else:
                continue
        x_coords = new_x_coords

    if x_coords:
        print('part 2:', x_coords, f'{row = }')
        print('part 2:', x_coords[0][0] * 4_000_000 + row)
        break
