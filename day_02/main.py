

assoziate_opponent = {'A': 'Rock', 'B': 'Paper', 'C': 'Scissors'}
assoziate_me = {'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}
score_shape = {'X': 1, 'Y': 2, 'Z': 3}
score_outcome = {'won': 6, 'draw': 3, 'lost': 0}

pattern_win = [['A', 'Y'], ['B', 'Z'], ['C', 'X']]
patter_draw = [['A', 'X'], ['B', 'Y'], ['C', 'Z']]

with open('input.txt', 'r') as f:
    data = f.read().strip()

rounds = [r.split() for r in data.split('\n')]

# part 1
total_score = 0

for r in rounds:
    if r in pattern_win:
        total_score += 6
    elif r in patter_draw:
        total_score += 3
    total_score += score_shape[r[1]]

print(total_score)

# part 2
choice_win = {'A': 'Y', 'B': 'Z', 'C': 'X'}
choice_draw = {'A': 'X', 'B': 'Y', 'C': 'Z'}
choice_lose = {'A': 'Z', 'B': 'X', 'C': 'Y'}

total_score = 0
for r in rounds:
    if r[1] == 'X':
        my_choice = choice_lose[r[0]]
        total_score += score_shape[my_choice]
    if r[1] == 'Y':
        my_choice = choice_draw[r[0]]
        total_score += 3
        total_score += score_shape[my_choice]
    if r[1] == 'Z':
        my_choice = choice_win[r[0]]
        total_score += 6
        total_score += score_shape[my_choice]

print(total_score)



