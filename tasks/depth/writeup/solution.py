import re
import requests

def visit(path):
    text = requests.get(path).text
    if "Index of" not in text:
        print(text)
        return

    for match in re.finditer(r"HREF=(\w+)/", text):
        word = match.group(1)
        visit(path + "/" + word)

visit("https://depth.q.2023.ugractf.ru/lkv2x8ejmsuxumkb")
