import pprint
import re
from typing import Self


class Velve:
    def __init__(self, name: str, pressure_release: int, next_velves_names: list[str]):
        self.name = name
        self.pressure_release = pressure_release
        self.next_velves: list[Self] = []
        self.remaining_time: int = 0
        self.next_velve_names = next_velves_names

    def __repr__(self):
        return (f'{self.__class__.__name__}(name: {self.name}, pressure_release: {self.pressure_release}, '
                f'next_velves: {self.next_velve_names})')


def parse_data(file: str) -> list[Velve]:
    result = {}
    with open(file, 'r') as f:
        data = f.readlines()

    for line in data:
        velve = re.findall(r'([A-Z]{2}|=(\d+))', line)
        (name, _), (_, pressure_release), *next_velves = velve
        next_velves = [v[0] for v in next_velves]
        result[name] = (Velve(name, pressure_release, next_velves))

    for v in result.values():
        v.next_velves = [result[n] for n in v.next_velve_names]

    return list(result.values())


def solve(file: str):
    velves = parse_data(file)
    pprint.pprint(velves)


if __name__ == '__main__':
    solve(file='test_input.txt')
