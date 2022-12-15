import re
from itertools import product

with open('test_input.txt', 'r') as f:
    data = [re.findall(r'-*\d+', l.strip()) for l in f.readlines()]
    data = [[(int(l[0]), int(l[1])), (int(l[2]), int(l[3]))] for l in data]

all_sensors_and_beacons = {p for pair in data for p in pair}

no_beacons = set()

for sensor, beacon in data:
    manh_dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    not_poss = {pos for pos in product(range(sensor[0]-manh_dist, sensor[0]+manh_dist+1),
                                       range(sensor[1]-manh_dist, sensor[1]+manh_dist+1))
                if (pos not in (sensor, beacon)
                    and abs(sensor[0] - pos[0]) + abs(sensor[1] - pos[1]) <= manh_dist)}
    print(manh_dist)
    print(sensor, beacon)
    print(not_poss)
    no_beacons |= not_poss

no_beacons = no_beacons - all_sensors_and_beacons
print(no_beacons)
curr_row = 10
not_poss_in_row = [p for p in no_beacons if p[1] == curr_row]
print(not_poss_in_row)
print(len(not_poss_in_row))
