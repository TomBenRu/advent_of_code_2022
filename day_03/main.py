import string

letters = {c: i for i, c in enumerate(string.ascii_letters, start=1)}

with open('input.txt', 'r') as f:
    data = f.read().strip()

# data = """vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg"""

data = data.split('\n')

# part 1
sum_priorities = 0
for items in data:
    items1, items2 = items[:len(items)//2], items[len(items)//2:]
    common_item = (set(list(items1)) & set(list(items2))).pop()
    sum_priorities += letters[common_item]

print(sum_priorities)

# part 2
sum_badge_priorities = 0
group = []
for items in data:
    group.append(set(list(items)))
    if len(group) == 3:
        common_item = (group[0] & group[1] & group[2]).pop()
        sum_badge_priorities += letters[common_item]
        group = []

print(sum_badge_priorities)





