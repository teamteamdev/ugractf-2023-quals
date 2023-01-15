import os.path
import re

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


def generate():
    code = ""

    flag = get_flag()

    with open("template.py") as f:
        for line in f.readlines():
            if "import" in line:
                exec(line)

            match = re.match(r"^if (.*) != \[\[VALUE\]\]:", line)
            if match:
                expr = match.group(1)
                line = line.replace("[[VALUE]]", repr(eval(expr)))
            code += line

    with open(os.path.join(get_attachments_dir(), "checker.py"), "w") as f:
        f.write(code)
