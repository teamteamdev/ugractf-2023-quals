import base64
import binascii
import bz2
import codecs
import gzip
import lzma
import os.path
import zstd

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


def generate():
    text = f"""Robert A. logged on

Josh logged on
Josh: one two one two do you read?

Robert A.: Yes sir!

Josh: finally, the damn thing works
Josh: It's been what, two months?

Robert A.: That's about right.

Josh: So how secure is this device anyway?

Robert A.: Certifications are still in progress, sir, but our cryptologists say even NSA wouldn't be able to crack it.
Robert A.: Von Stierlitz confirmed that too.

Josh: ah, Stierlitz.. I'm glad our security is in good hands
Josh: alright, transmitting the key now
Josh: {get_flag()}

Robert A.: Roger that, I will get back to you in five minutes, sir.
Robert A. left

Josh: von Stierlitz... I totally saw that name somewhere else
Josh: reminds me of Russia for some reason
Josh: nah, looks like a german name
Josh: maybe i just need to get some sleep

Josh left
""".encode()
    text = gzip.compress(text)
    text = codecs.encode(text, "uu")
    text = lzma.compress(text)
    text = binascii.hexlify(text)
    text = bz2.compress(text)
    text = base64.b32encode(text)
    text = zstd.compress(text)
    text = base64.b64encode(text)

    with open(os.path.join(get_attachments_dir(), "correspondence.txt"), "wb") as f:
        f.write(text)
