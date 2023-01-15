import base64
import os.path

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag, get_secret

import efficient_tortoisecrypt


def generate():
    attachments_dir = get_attachments_dir()
    password = get_secret("password")

    ciphertext = base64.b64encode(bytes(efficient_tortoisecrypt.crypt(get_flag().encode(), password.encode()))).decode()

    with open(os.path.join(attachments_dir, "password.txt"), "w") as f:
        f.write(f"{password}\n")
    with open(os.path.join(attachments_dir, "ciphertext.txt"), "w") as f:
        f.write(f"{ciphertext}\n")
