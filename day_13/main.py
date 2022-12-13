from copy import deepcopy

with open('input.txt', 'r') as f:
    data_1 = [part.split('\n') for part in f.read().split('\n\n')]

with open('input.txt', 'r') as f:
    data_2 = [part.strip() for part in f.read().split('\n') if part.strip()] + ['[[2]]'] + ['[[6]]']


def str2list(part: str):
    result = []
    parentesis_index = 0
    two_digits = False
    for i, c in enumerate(part):
        if two_digits:
            two_digits = False
            continue
        if c == '[':
            goal = result
            for _ in range(parentesis_index):
                goal = goal[-1]
            goal.append([])
            parentesis_index += 1
        elif c == ']':
            parentesis_index -= 1
        elif c.isnumeric():
            if part[i + 1].isnumeric():
                c += part[i + 1]
                two_digits = True
            goal = result
            for _ in range(parentesis_index):
                goal = goal[-1]
            goal.append(int(c))
    return result[0]


def proof_recursiv(l_val, r_val):
    def proof_lists(l_list, r_list):
        if l_list and not r_list:
            return False
        if not l_list and r_list:
            return True
        if not l_list and not r_list:
            return 'next'
        if l_list and r_list:
            result = proof_recursiv(l_list[0], r_list[0])
            if result == 'next':
                l_list.pop(0)
                r_list.pop(0)
                return proof_lists(l_list, r_list)
            else:
                return result

    if type(l_val) == type(r_val):
        if type(l_val) == int:
            if l_val < r_val:
                return True
            elif l_val > r_val:
                return False
            else:
                return 'next'
        elif type(l_val) == list:
            result = proof_lists(l_val, r_val)
            return result
    else:
        if type(l_val) == list:
            r_val = [r_val]
        else:
            l_val = [l_val]
        result = proof_lists(l_val, r_val)
        if result in (True, False):
            return result
        else:
            """goto next item"""
            return 'next'


def solfe_paket(packet: list[str]):
    left_p, right_p = packet
    left_list = str2list(left_p)
    right_list = str2list(right_p)
    return proof_recursiv(left_list, right_list)


result = 0
for i, p in enumerate(data_1, start=1):
    right_order = solfe_paket(p)
    if right_order:
        result += i

print(f'part 1: {result}')


data_2 = [str2list(part) for part in data_2]

changed = True
while changed:
    changed = False
    for i in range(len(data_2) - 1):
        if proof_recursiv(deepcopy(data_2[i]), deepcopy(data_2[i+1])):
            continue
        else:
            data_2[i], data_2[i + 1] = data_2[i + 1], data_2[i]
            changed = True

result_2 = 1
for i, data in enumerate(data_2, start=1):
    if data in ([[2]], [[6]]):
        result_2 *= i

print(f'part 2: {result_2}')
