import math
import re
import time


def read_puzzle(puzzle: str):
    with open(puzzle) as f:
        data = [list(map(int, re.findall(r'\d+', blueprint))) for blueprint in f.read().splitlines()]
        print(data)
    return data


def quality_heuristic(state):
    mined = state[3]
    return 1000 * mined[3] + 100 * mined[2] + 10 * mined[1] + mined[0]


def bfs(bp, robots, max_minutes, max_queue=500):
    """robots = tuple with ints for each robot, to calculate the materials which the robots can mine"""
    _, a, b, c, d, e, f = bp
    '''costs:[ore_robot, clay_robot, obsidion_robot, geode_robot]'''
    costs = [(a, 0, 0, 0), (b, 0, 0, 0), (c, d, 0, 0), (e, 0, f, 0)]  # (ore, clay, obsidion, geode)

    '''(minutes, robots, actual inventory of materials, sum of mined materials)'''
    queue = [(0, robots, (0, 0, 0, 0), (0, 0, 0, 0))]
    max_geodes_mined = depth = 0

    while queue:
        minutes, robots, inventory, mined = queue.pop(0)

        if minutes > depth:
            queue = sorted(queue, key=quality_heuristic, reverse=True)[:max_queue]
            depth = minutes
            # print(f'Munute {minutes} with {len(queue)} entries in queue')

        if minutes == max_minutes:
            max_geodes_mined = max(max_geodes_mined, mined[3])
            continue

        # new values for sum of mined materials is indepent of building or not
        new_mined = [mined[j] + robots[j] for j in range(4)]

        # try to build robots of each type
        for i in range(4):
            cost_robot = costs[i]

            # check if we have enough materials to biuld a robot, and append this new path to queue
            if all([inventory[j] >= cost_robot[j] for j in range(4)]):
                new_robots = list(robots)
                new_robots[i] += 1
                new_inventory = [inventory[j] - cost_robot[j] + robots[j] for j in range(4)]
                queue.append((minutes+1, new_robots, new_inventory, new_mined))

        # Do nothing, just mining
        new_inventory = [inventory[i] + robots[i] for i in range(4)]
        queue.append((minutes+1, robots, new_inventory, new_mined))

    return max_geodes_mined


def solve(puzzle):
    robots = (1, 0, 0, 0)
    part1 = sum(bp[0] * bfs(bp, robots, 24) for bp in puzzle)
    part2 = math.prod(bfs(bp, robots, 32) for bp in puzzle[:3])
    return part1, part2


if __name__ == '__main__':
    time_start = time.perf_counter()
    print(solve(read_puzzle('test_input.txt')))
    print(time.perf_counter() - time_start)
