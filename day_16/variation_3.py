import itertools
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
        self.opened_at_index: int | None = None

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
                f'next_velves: {self.next_velve_names}), closed: {self.closed}')


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


def shortest_path(start: Velve, end: Velve) -> list[Velve]:
    """Get the shortest path between 2 velves."""
    paths, visited, path_index = [[start]], {start.name}, 0
    while path_index < len(paths):
        curr_velve = paths[path_index][-1]
        for next_v in curr_velve.next_velves:
            if next_v.name == end.name:
                return paths[path_index]
            if next_v.name in visited:
                continue
            paths.append(paths[path_index].copy() + [next_v])
            visited.add(curr_velve.name)
        path_index += 1


def find_shortest_paths(velves: list[Velve]) -> dict[str, dict[str, list[Velve]]]:
    """Get a dictionary with the shortest paths between all velves."""
    path_lengths = {}
    for i, v1 in enumerate(velves):
        for v2 in velves[i+1:]:
            if not path_lengths.get(v1.name):
                path_lengths[v1.name] = {}
            if not path_lengths.get(v2.name):
                path_lengths[v2.name] = {}
            path_lengths[v1.name][v2.name] = shortest_path(v1, v2)
            path_lengths[v2.name][v1.name] = shortest_path(v2, v1)

    return path_lengths


def calculate_path_pressure_release(path: list[Velve], order_to_open: list[str], remaining_time: int) -> tuple[int, int]:
    result = 0
    for v in path:
        v.closed = True
    for i in range(len(path)):
        curr_velve = path[i]
        if remaining_time <= 0:
            break
        if curr_velve.closed and curr_velve.flow_rate and curr_velve.name == order_to_open[-1]:
            curr_velve.closed = False
            curr_velve.opened_at_index = i
            remaining_time -= 1
            result += remaining_time * curr_velve.flow_rate
            order_to_open.pop()
            # input(f'{curr_velve.name}: {curr_velve.flow_rate=}, {result=}, {remaining_time=}')
        if (i < len(path) - 1) and path[i+1].name in curr_velve.next_velve_names:
            remaining_time -= 1
            continue
        else:
            break
    return result, remaining_time


def find_next_rentable_velve(all_velves: list[Velve], start_velve: Velve, remaining_time: int,
                             shortest_paths: dict[str, list[Velve]]) -> tuple[Velve, list[Velve]] | None:
    best_pressure_release = 0
    best_next_velve = None

    for velve in all_velves:
        if velve == start_velve or not velve.flow_rate or not velve.closed:
            continue
        distance = len(shortest_paths[velve.name])
        effective_press_release = (remaining_time - distance - 1) * velve.flow_rate
        if effective_press_release > best_pressure_release:
            best_pressure_release = effective_press_release
            best_next_velve = velve
    if best_next_velve:
        return best_next_velve, shortest_paths[best_next_velve.name]


correct_test = ['AA', 'DD', 'CC', 'BB', 'AA', 'II', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'GG', 'FF', 'EE', 'DD', 'CC']


def find_optimal_route(velves: list[Velve], path_lengths: dict[str, dict[str, list[Velve]]], start: Velve, remaining_time):
    velves_dict: dict[str, Velve] = {v.name: v for v in velves}
    velve_flow_rates: dict[int, set[Velve]] = {}
    actuell_highest_result = 0
    path: list[Velve] = [start]
    fixe_velves = [start]

    velves_with_flowrate = [v for v in velves if v.flow_rate]
    max_pressure_release = 0
    path_with_max_pressure_release = ['AA']
    new_order = True
    while new_order:
        new_order = False
        for i in range(1, len(velves_with_flowrate) - 1):
            print('-------------------------------------------------------------------------------')
            velves_with_flowrate_new = velves_with_flowrate.copy()
            velves_with_flowrate_new[i-1], velves_with_flowrate_new[i] = velves_with_flowrate_new[i], velves_with_flowrate_new[i-1]
            print([v.name for v in velves_with_flowrate])
            print([v.name for v in velves_with_flowrate_new])
            path_1 = []
            for a, b in itertools.pairwise(velves_with_flowrate):
                path_1.extend(shortest_path(a, b))
            path_1 = [start] + path_1
            path_1.append(velves_with_flowrate[-1])
            path_2 = []
            for a, b in itertools.pairwise(velves_with_flowrate_new):
                path_2.extend(shortest_path(a, b))
            curr_path = [start] + path_2
            curr_path.append(velves_with_flowrate_new[-1])

            press_rel_1, rest_time_1 = calculate_path_pressure_release(path_1, [v.name for v in velves_with_flowrate][::-1], 30)
            press_rel_2, rest_time_2 = calculate_path_pressure_release(path_2, [v.name for v in velves_with_flowrate_new][::-1], 30)

            if press_rel_1 > press_rel_2:
                continue
            else:
                velves_with_flowrate = velves_with_flowrate_new.copy()
                new_order = True
        print([v.name for v in velves_with_flowrate])
    print([v.name for v in velves_with_flowrate])




def solve(file: str):
    velves, start = parse_data(file)
    # pprint.pprint(velves)
    path_lengths = find_shortest_paths(velves)
    # pprint.pprint(path_lengths)
    find_optimal_route(velves, path_lengths, start, 30)




if __name__ == '__main__':
    solve(file='test_input.txt')
