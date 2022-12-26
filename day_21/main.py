from copy import deepcopy


def read_input(file: str):
    with open(file) as f:
        data = {name: (int(operation) if operation.isnumeric() else operation) for name, operation in [m.split(': ') for m in f.read().splitlines()]}
    return data


def get_result_of_operation(monkey_1: int, operator: str, monkey_2: int):
    return eval(f'{monkey_1} {operator} {monkey_2}')


def solve(monkeys: dict[str, str | int], root: str) -> int:
    if type(monkeys[root]) == int:
        return monkeys[root]

    monkey_1, operator, monkey_2 = monkeys[root].split()

    num_1, num_2 = solve(monkeys, monkey_1), solve(monkeys, monkey_2)
    result = get_result_of_operation(num_1, operator, num_2)
    if root == 'root':
        print(num_1, num_2, result)
    return result


if __name__ == '__main__':
    data = read_input('input.txt')
    print(data)

    monkeys = deepcopy(data)

    result = solve(monkeys, 'root')
    print(result)

    # part 2
    original = data['root'].split()
    data['root'] = original[0] + ' == ' + original[2]

    zahl = 3_403_989_691_757
    print(zahl)
    for z in range(zahl, zahl+1):
        data['humn'] = z
        res = solve(data, 'root')
        print(f'{res=}')
        if res is True:
            print(f'Your number is: {z}')
            break
