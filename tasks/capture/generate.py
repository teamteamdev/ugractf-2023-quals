#!/usr/bin/env python3

import hmac
import random
import subprocess
import json
import sys
import os

PREFIX = "ugra_traffic_extractor_"
TOKEN_SECRET = b"kcR7WlhtJdi4N2hmti/p6w=="
TOKEN_SIZE = 16
FLAG_SECRET = b"Ls6HrZTgjT7xQKmifSQO1w=="
SUFFIX_SIZE = 12

def get_user_tokens(user_id):
    token = hmac.new(TOKEN_SECRET, str(user_id).encode(), "sha256").hexdigest()[:TOKEN_SIZE]
    flag = PREFIX + hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]
    
    return token, flag

def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    attachments = os.path.join(sys.argv[2], "attachments")
    token, flag = get_user_tokens(user_id)
    
    #gen_env = os.environ.copy()
    #gen_env["FLAG"] = flag
    subprocess.run(["./pcap_generator/gen_pcap.sh", flag, attachments], check=True)

    json.dump({
        "flags": [flag]
    }, sys.stdout)

if __name__ == "__main__":
    generate()
