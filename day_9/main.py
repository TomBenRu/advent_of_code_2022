
def steps(vec: list[int]):
    x, y = vec
    if x != 0:
        for _ in range(abs(x)):
            yield [1 if x > 0 else -1, y]
    elif y != 0:
        for _ in range(abs(y)):
            yield [x, 1 if y > 0 else -1]
    else:
        yield [x, y]


def pull(head: list[int], tail: list[int]):
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return tail
    else:
        x = tail[0] if (head[0] - tail[0]) == 0 else (head[0] - tail[0]) // abs(head[0] - tail[0]) + tail[0]
        y = tail[1] if (head[1] - tail[1]) == 0 else (head[1] - tail[1]) // abs(head[1] - tail[1]) + tail[1]
        return [x, y]


def add_vector(v1: list[int], v2: list[int]):
    return [v1[0] + v2[0], v1[1] + v2[1]]


with open('input.txt', 'r') as f:
    data = [l.strip().split() for l in f.readlines()]

moves = [[int(steps), 0] if direction == 'R'
         else ([-int(steps), 0] if direction == 'L'
               else ([0, int(steps)] if direction == 'U' else [0, -int(steps)])) for direction, steps in data]

print(moves)

# part 1
visited = set()

curr_tail, curr_head = knots = [[0, 0], [0, 0]]
visited.add(tuple(curr_tail))

for move in moves:
    for step in steps(move):
        curr_head = add_vector(curr_head, step)
        curr_tail = pull(curr_head, curr_tail)
        visited.add(tuple(curr_tail))

print(len(visited))

# part 2

knots = [[0, 0] for _ in range(10)]
visited = set()
visited.add((0, 0))

for move in moves:
    for step in steps(move):
        knots[0] = add_vector(knots[0], step)
        for i in range(1, 10):
            knots[i] = pull(knots[i-1], knots[i])
        visited.add(tuple(knots[9]))

print(len(visited))

