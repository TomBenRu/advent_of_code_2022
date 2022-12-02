

with open('input.txt', 'r') as f:
    data = f.read().strip()

# part 1
max_calories = max([sum([int(c) for c in elve_part.split('\n')]) for elve_part in data.split('\n\n')])
print(max_calories)

# part 2
max_calories_top_3 = sum(sorted([sum([int(c) for c in elve_part.split('\n')]) for elve_part in data.split('\n\n')])[-3:])
print(max_calories_top_3)
