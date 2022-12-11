import math


class Monkey:
    def __init__(self, starting_items: list[int], operation: str, test_div: int, worry_level_div: int,
                 monkey_true: int, monkey_false: int):
        self.starting_items = starting_items
        self.test_div = test_div
        self.worry_level_div = worry_level_div
        self.operation = operation
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.inspected = 0
        self.modulo_number = None

    def throw(self):
        for item in self.starting_items:
            self.inspected += 1
            worry_level = (eval(self.operation, {}, {'old': item}) // self.worry_level_div) % self.modulo_number
            if not worry_level % self.test_div:
                monkeys[self.monkey_true].starting_items.append(worry_level)
            else:
                monkeys[self.monkey_false].starting_items.append(worry_level)
        self.starting_items = []

    def __repr__(self):
        return f'({self.starting_items = }, {self.operation = }, {self.test_div = }, {self.monkey_true = }, {self.monkey_false = })'


with open('input.txt', 'r') as f:
    monkey_datas = [{p.strip().split(':')[0]: p.strip().split(':')[1].strip() for p in m.split('\n')[1:]} for m in f.read().split('\n\n')]

# part 1
monkeys: list[Monkey] = []

for m_data in monkey_datas:
    monkey = Monkey(starting_items=[int(item) for item in m_data['Starting items'].split(', ')],
                    operation=m_data['Operation'].split(' = ')[1],
                    test_div=int(m_data['Test'].split()[-1]),
                    worry_level_div=3,
                    monkey_true=int(m_data['If true'].split()[-1]),
                    monkey_false=int(m_data['If false'].split()[-1]))
    monkeys.append(monkey)
modulo_number = math.prod([m.test_div for m in monkeys])
for m in monkeys:
    m.modulo_number = modulo_number

for _ in range(20):
    for m in monkeys:
        m.throw()

most_active = sorted(m.inspected for m in monkeys)[-2:]
print(most_active[0] * most_active[1])


# part 2
monkeys: list[Monkey] = []

for m_data in monkey_datas:
    monkey = Monkey(starting_items=[int(item) for item in m_data['Starting items'].split(', ')],
                    operation=m_data['Operation'].split(' = ')[1],
                    test_div=int(m_data['Test'].split()[-1]),
                    worry_level_div=1,
                    monkey_true=int(m_data['If true'].split()[-1]),
                    monkey_false=int(m_data['If false'].split()[-1]))
    monkeys.append(monkey)

modulo_number = math.prod([m.test_div for m in monkeys])
for m in monkeys:
    m.modulo_number = modulo_number

for _ in range(10_000):
    for m in monkeys:
        m.throw()

most_active = sorted(m.inspected for m in monkeys)[-2:]
print(most_active[0] * most_active[1])
