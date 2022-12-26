import pprint
import re
import time
from copy import deepcopy

with open('test_input.txt') as f:
    data = [re.findall(r'\d+', blueprint) for blueprint in f.read().splitlines()]

blueprints = {int(bp[0]): {'ore_robot': {'ore': int(bp[1])},
                           'clay_robot': {'ore': int(bp[2])},
                           'obsidian_robot': {'ore': int(bp[3]), 'clay': int(bp[4])},
                           'geode_robot': {'ore': int(bp[5]), 'obsidian': int(bp[6])}}
              for bp in data}

pprint.pprint(blueprints)

most_geode = 0
def search_best_prod_path(blueprint_nr: int, robots: dict[str, int], collected: dict[str, int], time_spended: int):
    global most_geode
    if collected['geode'] > most_geode:
        most_geode = collected['geode']

    blueprint = blueprints[blueprint_nr]

    if time_spended == 24:
        return collected['geode']
    producable = []
    for to_produce, materials in blueprint.items():
        for needed_stuff, nr_st in materials.items():
            if collected[needed_stuff] < nr_st:
                break
        else:
            producable.append(to_produce)
    for robot, nr_r in robots.items():
        material = robot.split('_')[0]
        for _ in range(nr_r):
            collected[material] += 1

    coll_geodes = []

    for rob in producable:
        robots_copy = deepcopy(robots)
        robots_copy[rob] += 1
        collected_copy = deepcopy(collected)
        for stuff, n in blueprint[rob].items():
            collected_copy[stuff] -= n
        geodes = search_best_prod_path(blueprint_nr, robots_copy, collected_copy, time_spended + 1)
        coll_geodes.append(geodes)
    if len(producable) < 4:
        geodes = search_best_prod_path(blueprint_nr, deepcopy(robots), deepcopy(collected), time_spended + 1)
        coll_geodes.append(geodes)
    if time_spended < 14:
        print(f'{time_spended = }')
        print(f'{most_geode = }')
    return max(coll_geodes)


if __name__ == '__main__':
    search_best_prod_path(2,
                          robots={'clay_robot': 0, 'geode_robot': 0, 'obsidian_robot': 0, 'ore_robot': 1},
                          collected={'clay': 0, 'geode': 0, 'obsidian': 0, 'ore': 0},
                          time_spended=0
                          )
