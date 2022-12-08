import re
from typing import Self


class Directory:
    def __init__(self, parent):
        self.parent = parent

        self.directories: list[Self] = []
        self.files: list[int] = []

    @property
    def size(self):
        return sum(self.files) + sum([d.size for d in self.directories])


root = Directory(parent=None)

directories = []

curr_directory: Directory = root

with open('input.txt', 'r') as f:
    data = f.readlines()

for line in data[1:]:
    curr = line.strip().split(' ')
    if curr[0] == '$':
        if curr[1] == 'cd':
            if curr[2] == '/':
                curr_directory = root
            elif curr[2] == '..':
                curr_directory = curr_directory.parent
            else:
                new_dir = Directory(curr_directory)
                curr_directory.directories.append(new_dir)
                curr_directory = new_dir
                if new_dir not in directories:
                    directories.append(new_dir)
        else:
            continue
    else:
        if (curr[0]).isdigit():
            curr_directory.files.append(int(curr[0]))

# part 1
print(sum(d.size for d in directories if d.size <= 100_000))

# part 2

total_disk_space = 70_000_000
unused_space = 30_000_000
actual_free = total_disk_space - root.size
space_to_free_up = unused_space - actual_free

to_delete = float('inf')
for d in directories:
    if to_delete >= d.size >= space_to_free_up:
        to_delete = d.size

print(to_delete)
