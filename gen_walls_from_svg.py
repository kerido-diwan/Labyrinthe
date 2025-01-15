#! /usr/bin/env python3
import re

walls = []

with open('lab2.svg') as file:
    for l in file.readlines():
        match = re.search(r'x1="(\d+)" y1="(\d+)" x2="(\d+)" y2="(\d+)"', l)
        if match is None:
            continue
        x1, y1, x2, y2 = match.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        walls.append([x1 - 2, y1 - 2, x2, y2])


with open('lab2.orig.tmx') as file:
    tmx_lines = file.readlines()

ids = []
for l in tmx_lines:
    match = re.search(r'id="(\d+)"', l)
    if match is None:
        continue
    ids.append(int(match.group(1)))

id_ = max(ids) + 1

with open('lab2.tmx', "w") as output:
    output.write(''.join(tmx_lines[:-2]))
    for x1, y1, x2, y2 in walls:
        x = x1
        y = y1
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        id_ = id_ + 1
        output.write(f'<object id="{id_}" type="collision" x="{x}" y="{y}" width="{width}" height="{height}"/>\n')
    output.write(''.join(tmx_lines[-2:]))

print(f"Successfully wrote {len(tmx_lines) + len(walls)} lines.")
