#! /usr/bin/env python3

from pathlib import Path
import re

DIR = Path(__file__).parent.parent

INPUT_DIR = DIR / "maps_input"
OUTPUT_DIR = DIR / "assets"


def gen_file(svg_file, orig_tmx_file, output_tmx_file):
    walls = []
    print(f'gen_file({svg_file}, {orig_tmx_file}, {output_tmx_file}')
    with open(svg_file) as file:
        for l in file.readlines():
            match = re.search(r'x1="(\d+)" y1="(\d+)" x2="(\d+)" y2="(\d+)"', l)
            if match is None:
                continue
            x1, y1, x2, y2 = match.groups()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            walls.append([x1 - 2, y1 - 2, x2, y2])


    with open(orig_tmx_file) as file:
        tmx_lines = file.readlines()

    ids = []
    for l in tmx_lines:
        match = re.search(r'id="(\d+)"', l)
        if match is None:
            continue
        ids.append(int(match.group(1)))

    id_ = max(ids) + 1

    with open(output_tmx_file, "w") as output:
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


for file in INPUT_DIR.iterdir():
    if file.suffix == ".svg":
        map_name = file.stem
        tmx_file = INPUT_DIR / (map_name + ".orig.tmx")
        output_tmx_file = OUTPUT_DIR / (map_name + ".tmx")
        gen_file(file, tmx_file, output_tmx_file)
