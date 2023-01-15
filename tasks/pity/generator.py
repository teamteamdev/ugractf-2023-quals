import os.path
import random
import json

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


WIDTH = 64


def render_text(text):
    with open("seven-plus.json") as f:
        font = json.load(f)

    lines = [""] * max(font["lineHeight"], max(glyph["offset"] + len(glyph["pixels"]) for glyph in font["glyphs"].values()))

    for c in text:
        glyph = font["glyphs"][c]
        for i in range(len(lines)):
            j = i - glyph["offset"]
            if 0 <= j < len(glyph["pixels"]):
                line = "".join("█" if c else " " for c in glyph["pixels"][j])
            else:
                line = " " * len(glyph["pixels"][0])
            lines[i] += line + " "

    while lines[-1].strip() == "":
        lines.pop()

    return lines


def generate():
    lines = render_text(get_flag())

    result = ""

    for scroll in range(len(lines[0]) + WIDTH):
        picture = [
            (line + " " * WIDTH)[:scroll][-WIDTH:].rjust(WIDTH)
            for line in lines
        ]
        for _ in range(2):  # artificial delay
            yy = list(range(len(picture)))
            random.shuffle(yy)
            for y in yy:
                xx = list(range(WIDTH))
                random.shuffle(xx)
                for x in xx:
                    result += f"\x1b[{y + 1};{x + 1}H" + picture[y][x]

    with open(os.path.join(get_attachments_dir(), "movie.txt"), "w") as f:
        f.write(result)
