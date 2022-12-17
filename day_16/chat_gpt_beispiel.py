import re
import sys

sys.setrecursionlimit(100_000)


class Velve:
    def __init__(self, name: str, flow_rate: int, next_velve_names: list[str]):
        self.name = name
        self.flow_rate = flow_rate
        self.next_velve_names = next_velve_names

    def __repr__(self):
        return f'({self.flow_rate=}, {self.next_velve_names=})'


def parse_data(file: str):
    with open(file, 'r') as f:
        data = f.readlines()

    for line in data:
        velve = re.findall(r'([A-Z]{2}|=(\d+))', line)
        (name, _), (_, flow_rate), *next_velves = velve
        next_velves = [v[0] for v in next_velves]
        velves[name] = Velve(name, int(flow_rate), next_velves)
    print(velves)


# Function to explore all possible paths through the building
def explore_paths(current_velve, time_remaining, pressure_released, path):
    # If there is enough time remaining, switch on the machine in the current room
    # and add the number of candies it produces to the total count
    if time_remaining >= 1:
        rate = velves[current_velve].flow_rate
        pressure_released += time_remaining * rate

    # Update the maximum number of candies produced and the path taken to reach it
    # if the current path produces more candies than the maximum found so far
    global max_pressure_released, max_path
    if pressure_released > max_pressure_released:
        max_pressure_released = pressure_released
        max_path = path

    # Loop through all rooms connected to the current room
    for next_velve in velves[current_velve].next_velve_names:
        # Explore the path starting from the next room
        explore_paths(next_velve, time_remaining - 1, pressure_released, path + [next_velve])


# Data structure to represent the velves and connections between them
velves: dict[str, Velve] = {}


# Initialize the maximum released pressure and the path taken to reach it
max_pressure_released = 0
max_path = []


if __name__ == '__main__':
    # Parse Data from file and put it to the datastructure
    parse_data('test_input.txt')
    # Start exploring paths from the start room
    start_velve = "AA"
    explore_paths(start_velve, 30, 0, [start_velve])

    # Print the path that leads to the maximum number of candies produced
    print(max_path)
