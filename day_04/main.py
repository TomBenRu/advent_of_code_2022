


with open('input.txt', 'r') as f:
    data = f.read().strip()

data = [[[int(n) for n in e.split('-')] for e in line.split(',')] for line in data.split('\n')]

print(data)

nbrs_of_fully_intersection = 0
nbrs_of_intersection = 0
for section_a, section_b in data:
    nbrs_a = set(range(section_a[0], section_a[1]+1))
    nbrs_b = set(range(section_b[0], section_b[1]+1))
    if (nbrs_a | nbrs_b) in (nbrs_a, nbrs_b):
        nbrs_of_fully_intersection += 1
    if nbrs_a & nbrs_b:
        nbrs_of_intersection += 1

print(nbrs_of_fully_intersection)
print(nbrs_of_intersection)
