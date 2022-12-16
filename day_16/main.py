import math
import pprint
import random
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from typing import Self


class Velve:
    def __init__(self, name: str, flow_rate: int, next_velves_names: list[str], remaining_time: int):
        self.name = name
        self.flow_rate: int = flow_rate
        self.next_velves: list[Self] = []
        self.remaining_time: int = remaining_time
        self.path_index: int | None = None
        self.total_pressure_release: int = 0
        self.next_velve_names = next_velves_names
        self.closed: bool = True

    @property
    def pressure_release(self):
        return self.remaining_time * self.flow_rate

    def set_values(self, remaining_time: int = None, path_index: int = None, total_pressure_release: int = None):
        if remaining_time:
            self.remaining_time = remaining_time
        if path_index:
            self.path_index = path_index
        if total_pressure_release:
            self.total_pressure_release = total_pressure_release

    def __repr__(self):
        return (f'{self.__class__.__name__}(name: {self.name}, pressure_release: {self.flow_rate}, '
                f'next_velves: {self.next_velve_names})')


def parse_data(file: str) -> tuple[list[Velve], Velve]:
    result = {}
    start_velve: Velve | None = None
    with open(file, 'r') as f:
        data = f.readlines()

    for line in data:
        velve = re.findall(r'([A-Z]{2}|=(\d+))', line)
        (name, _), (_, flow_rate), *next_velves = velve
        next_velves = [v[0] for v in next_velves]
        result[name] = (curr := (Velve(name, int(flow_rate), next_velves, 30)))
        if name == 'AA':
            start_velve = curr

    for v in result.values():
        v.next_velves = [result[n] for n in v.next_velve_names]

    return list(result.values()), start_velve


def path_length(start: Velve, end: Velve) -> int:
    """Get the shortest path between 2 velves."""
    paths, visited, path_index = [[start]], {start.name}, 0
    while path_index < len(paths):
        curr_velve = paths[path_index][-1]
        for next_v in curr_velve.next_velves:
            if next_v.name == end.name:
                return len(paths[path_index])
            if next_v.name in visited:
                continue
            paths.append(paths[path_index].copy() + [next_v])
            visited.add(curr_velve.name)
        path_index += 1


def find_shortest_paths(velves: list[Velve]) -> dict[str, dict[str, int]]:
    """Get a dictionary with the shortest paths between all velves."""
    path_lengths = {}
    for i, v1 in enumerate(velves):
        for v2 in velves[i+1:]:
            if not path_lengths.get(v1.name):
                path_lengths[v1.name] = {}
            if not path_lengths.get(v2.name):
                path_lengths[v2.name] = {}
            path_lengths[v1.name][v2.name] = path_length(v1, v2)
            path_lengths[v2.name][v1.name] = path_length(v2, v1)

    return path_lengths


def calculate_path_pressure_release(path: dict[int, Velve], remaining_time: int = 30) -> int:
    result = 0
    for i in range(30):
        curr_velve = path[i]
        if remaining_time <= 0:
            break
        if curr_velve.closed and curr_velve.flow_rate:
            curr_velve.closed = False
            remaining_time -= 1
            result += remaining_time * curr_velve.flow_rate
        if path[i+1].name in curr_velve.next_velve_names:
            remaining_time -= 1
            continue
        else:
            break
    return result


def anealing(val_old: int, val_new: int, t: int) -> bool:
    if val_new >= val_old:
        return True
    try:
        a = math.exp(-(val_old - val_new) / t)
    except:
        a = 0
    # input(f'{val_new = }, {val_old = }, {t = }, {a = }')
    if a > random.random():
        return True


def find_optimal_route(velves: list[Velve], path_lengths: dict[str, dict[str, int]], start: Velve, remaining_time):
    t_for_anealing = 100
    velves_dict: dict[str, Velve] = {v.name: v for v in velves}
    velve_flow_rates: dict[int, set[Velve]] = {}
    actuell_highest_result = 0
    path: dict[int: Velve] = {0: start, 1: velves_dict['BB']} | {i: random.choice(velves) for i in range(2, 29)}

    loop_num = 0
    while True:
        loop_num += 1
        if not loop_num % 1000:
            t_for_anealing /= 1.001
        for v in velves:
            v.closed = True
        new_v1, new_v2 = random.choice(velves), random.choice(velves)
        idx1, idx2 = random.sample(range(2, 29), 2)
        old_v1, old_v2 = path[idx1], path[idx2]
        path[idx1], path[idx2] = new_v1, new_v2
        # if path[1].name == 'DD':
        #     input(f'{path[0]} -> {path[1]}')
        for v in path.values():
            v.closed = True
        # print(path)
        result = calculate_path_pressure_release(path)
        if not anealing(actuell_highest_result, result, t_for_anealing):
            path[idx1], path[idx2] = old_v1, old_v2
        else:
            actuell_highest_result = result
        if not loop_num % 100_000:
            print(f'{actuell_highest_result = }')
            print(f'{t_for_anealing = }')







def solve(file: str):
    velves, start = parse_data(file)
    # pprint.pprint(velves)
    path_lengths = find_shortest_paths(velves)
    pprint.pprint(path_lengths)
    find_optimal_route(velves, path_lengths, start, 30)




if __name__ == '__main__':
    solve(file='test_input.txt')
