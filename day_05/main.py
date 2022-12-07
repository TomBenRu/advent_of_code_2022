import re

with open('input.txt', 'r') as f:
    stacks, commands = f.read().split('\n\n')

stacks = {int(stack[-1]): [c for c in stack[:-1][::-1] if c != ' '] for stack in zip(*[[l[i] for i in range(1, 34, 4)]
                                                                                       for l in stacks.splitlines()])}
stacks_copy: dict[int, list] = {k: v[:] for k, v in stacks.items()}

commands = [[int(v) for v in re.findall(r'\d+', c)] for c in commands.splitlines()]

# part 1
for command in commands:
    for _ in range(command[0]):
        stacks[command[2]].append((stacks[command[1]].pop()))

print(''.join([stack[-1] for stack in stacks.values()]))

# part 2
for command in commands:
    stacks_copy[command[2]].extend(stacks_copy[command[1]][-command[0]:])
    stacks_copy[command[1]] = stacks_copy[command[1]][:-command[0]]

print(''.join([stack[-1] for stack in stacks_copy.values()]))

