from kyzylborda_lib.secrets import get_flag

from encrypt import encrypt_flag


def generate():
    return {
        "bullets": [encrypt_flag(get_flag())]
    }
