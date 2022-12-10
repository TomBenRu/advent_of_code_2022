
def cycles_to_watch():
    c = 20
    yield c
    while True:
        c += 40
        yield c


with open('input.txt', 'r') as f:
    data = [instr.strip() for instr in f.readlines()]

cycle = 0
value_x = 1
signal_strengths = []
ctw = cycles_to_watch()
actual_ctw = next(ctw)

pixels = ''

for line in data:
    if line == 'noop':
        cycle += 1
        v = 0

        if ((cycle - 1) % 40) in (value_x-1, value_x, value_x+1):
            pixels += '#'
        else:
            pixels += '.'

    else:
        v = int(line.split()[1])
        for _ in range(2):
            cycle += 1

            if ((cycle - 1) % 40) in (value_x-1, value_x, value_x+1):
                pixels += '#'
            else:
                pixels += '.'

    if cycle >= actual_ctw:
        signal_strengths.append(actual_ctw * value_x)
        actual_ctw = next(ctw)
    value_x += v

# part 1
print(f'{sum(signal_strengths) = }')

# part 2
for i in range(40, 241, 40):
    print(pixels[i-40: i])


