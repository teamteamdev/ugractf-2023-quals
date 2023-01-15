#!/usr/bin/env python3

import hmac
import json
import sys
import tempfile

import PIL.Image, PIL.ImageDraw, PIL.ImageFont
import random
import os
import subprocess

PREFIX = "ugra_we_support_local_artists_"
FLAG_SECRET = b"it's only teenage wasteland"
SUFFIX_SIZE = 6

def get_flag(user_id):
    flag = PREFIX + hmac.new(FLAG_SECRET, user_id.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]
    return flag

def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file = sys.stderr)
        sys.exit(1)
    
    user_id = sys.argv[1]
    flag = get_flag(user_id)
    target_dir = sys.argv[2]

    random.seed(hmac.new(FLAG_SECRET, user_id.encode(), "sha256").digest())

    FONT = PIL.ImageFont.load(os.path.join("private", "Galmuri11-Bold.pil"))

    positions = [list(range(i * 6, (i + 1) * 6)) for i in range(0, 6)]
    offsets = [[(random.randint(-6, 6), random.randint(-3, 3)) for j in range(0, 6)] for i in range(0, 6)]

    for n in range(13):
        x, y = random.randint(0, 4), random.randint(0, 4)
        if n % 2:
            nx, ny = x + 1, y
        else:
            continue
            nx, ny = x, y + 1
        positions[x][y], positions[nx][ny] = positions[nx][ny], positions[x][y]

    image = PIL.Image.new("RGB", (180, 180))
    draw = PIL.ImageDraw.ImageDraw(image)

    def find_position(n):
        X, Y = 0, 0
        for x in range(0, 6):
            for y in range(0, 6):
                if positions[x][y] == n:
                    X, Y = x, y
        return 15 + X * 30 + offsets[X][Y][0], 15 + Y * 30 + offsets[X][Y][1]

    X, Y = find_position(0)
    RAINBOW = [(255, 0, 0), (255, 89, 0), (255, 179, 0), (240, 255, 0), (150, 255, 0), (60, 255, 0),
               (0, 255, 30), (0, 255, 120), (0, 255, 209), (0, 209, 255), (0, 120, 255), (0, 29, 255),
               (60, 0, 255), (149, 0, 255), (240, 0, 255), (255, 0, 180), (255, 0, 90), (255, 0, 0),
               (255, 90, 0), (255, 180, 0), (240, 255, 0), (149, 255, 0), (59, 255, 0), (0, 255, 29),
               (0, 255, 120), (0, 255, 210), (0, 210, 255), (0, 120, 255), (0, 29, 255), (59, 0, 255),
               (149, 0, 255), (240, 0, 255), (255, 0, 180), (255, 0, 90), (255, 0, 0)]

    for i in range(1, 36):
        x, y = find_position(i)
        draw.line((X, Y, x, y), fill=RAINBOW[i - 1])
        X, Y = x, y

    for x in range(0, 6):
        for y in range(0, 6):
            draw.text((15 + x * 30 - 3 + offsets[x][y][0], 15 + y * 30 - 5 + offsets[x][y][1]),
                      flag[positions[x][y]], font=FONT, fill=(255, 255, 255))

    image = image.resize((1200, 1200), PIL.Image.NEAREST)
    with tempfile.TemporaryDirectory() as d:
        image.save(os.path.join(d, "albumart.png"), format="png")

        os.makedirs(os.path.join(target_dir, "static"), exist_ok=True)
        subprocess.check_call(["ffmpeg", "-y", "-i", os.path.join("private", "song.mp3"),
                               "-i", os.path.join(d, "albumart.png"),
                               *"-map 0:0 -map 1:0 -id3v2_version 3 -metadata".split(),
                               "artist=ксикки", "-metadata", "title=стф песня",
                               "-metadata", "publisher=новая () метта", "-c:a", "copy",
                               os.path.join(target_dir, "static", "6574_ksikky_-_stf_pesny_(radio_edit)_320kbps.mp3")])

    json.dump({"flags": [flag]}, sys.stdout)

if __name__ == "__main__":
    generate()
