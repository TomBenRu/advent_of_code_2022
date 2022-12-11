from typing import Callable


class Monkey:
    def __init__(self, starting_items: list[int], operation: str, test_div: int,
                 monkey_true: int, monkey_false: int):
        self.starting_items = starting_items
        self.test_div = test_div
        self.operation = operation
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false

    def throw(self):
        for item in self.starting_items[::-1]:
            worry_level = eval(self.operation, {}, {'old': item}) // 3
            if not worry_level % self.test_div:
                monkeys[self.monkey_true].starting_items.append(worry_level)
            else:
                monkeys[self.monkey_false].starting_items.append(worry_level)


monkeys: list[Monkey] = []

with open('test_input.txt', 'r') as f:
    monkey_datas = [{p.strip().split(':')[0]: p.strip().split(':')[1].strip() for p in m.split('\n')[1:]} for m in f.read().split('\n\n')]

print(monkey_datas)

for m_data in monkey_datas:
    monkey = Monkey(starting_items=[int(item) for item in m_data['Starting items'].split(', ')],
                    operation=m_data['Operation'].split(' = ')[1],
                    test_div=int(m_data['Test'].split()[-1]),
                    monkey_true=int(m_data['If true'].split()[-1]),
                    monkey_false=int(m_data['If false'].split()[-1]))
    monkeys.append(monkey)

print(monkeys)
