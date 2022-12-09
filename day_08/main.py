
with open('input.txt', 'r') as f:
    trees = [[int(t) for t in list(row.strip())] for row in f.readlines()]

width = len(trees[0])
height = len(trees)

# part 1
visible_trees = 0
for row_index, row in enumerate(trees):
    for tree_index, tree in enumerate(row):
        if row_index in (0, height-1) or tree_index in (0, width-1):
            visible_trees += 1
            continue
        if max(row[:tree_index]) < tree or tree > max(row[tree_index+1:]):
            visible_trees += 1
            continue
        column = list(zip(*trees[::-1]))[tree_index][::-1]
        if max(column[:row_index]) < tree or tree > max(column[row_index+1:]):
            visible_trees += 1
            continue

print(f'{visible_trees = }')

# part 2
scenic_core: int = 0

for row_index, row in enumerate(trees):
    for tree_index, tree in enumerate(row):
        if row_index in (0, height - 1) or tree_index in (0, width - 1):
            continue
        left, right, up, down = 1, 1, 1, 1
        # walking left and right:
        if tree_index == 1:
            left = 1
        else:
            for x in range(tree_index-1, 0, -1):
                if row[x] < tree:
                    left += 1
                else:
                    break
        if tree_index == width - 2:
            right = 1
        else:
            for x in range(tree_index+1, width-1):
                if row[x] < tree:
                    right += 1
                else:
                    break
        # walking up and down:
        column = list(zip(*trees[::-1]))[tree_index][::-1]
        if row_index == 1:
            up = 1
        else:
            for y in range(row_index-1, 0, -1):
                if column[y] < tree:
                    up += 1
                else:
                    break
        if row_index == height - 2:
            down = 1
        else:
            for y in range(row_index + 1, height-1):
                if column[y] < tree:
                    down += 1
                else:
                    break
        if (new_score := (left * right * up * down)) > scenic_core:
            scenic_core = new_score
print(f'{scenic_core = }')



