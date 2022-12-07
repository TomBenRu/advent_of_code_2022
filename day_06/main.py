

with open('input.txt', 'r') as f:
    data = f.read()

# part 1
for i, c in enumerate(data[3:], start=3):
    if len(set(data[i-3:i+1])) != 4:
        continue
    print(i + 1, data[i-3: i+1])
    break

# part 2
for i, c in enumerate(data[13:], start=13):
    if len(set(data[i-13:i+1])) != 14:
        continue
    print(i + 1, data[i-13: i+1])
    break
