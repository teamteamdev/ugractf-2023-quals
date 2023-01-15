#!/usr/bin/env python3

import hmac
import random
import json
import sys
import os
import subprocess

PREFIX = "ugra_oneliners_rule_"
TOKEN_SECRET = b"N2UyNzk2MjQ0ZjU3NDgwNDg0MjdjMTM5"
TOKEN_SIZE = 16
FLAG_SECRET = b"ODNkNjIyMjNhZWExNDA5OTkwYzM1NGQ1"
SUFFIX_SIZE = 12
KEY_SECRET = b"YjQ5YzkwYjNmZjdlNDBlNTk5Y2RmYWFh"
KEY_SIZE = 12

def get_user_tokens(user_id):
    token = hmac.new(TOKEN_SECRET, str(user_id).encode(), "sha256").hexdigest()[:TOKEN_SIZE]
    flag = PREFIX + hmac.new(FLAG_SECRET, token.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]
    key = hmac.new(KEY_SECRET, str(user_id).encode(), "sha256").hexdigest()[:KEY_SIZE]

    return token, flag, key

def generate_bash_history_entry(p):
        directories = [
            "/",
            "/etc/",
            "/etc/apt/",
            "/etc/network/",
            "/etc/systemd/system/",
            "/home/user/",
            "/home/user/.ssh/",
            "/home/user/Downloads/",
            "/home/user/Documents/",
            "/mnt/",
            "/mnt/fleshka/",
            "/mnt/zhostkiy_disk/",
            "/mnt/zhostkiy_disk/vazhnoe/",
            "/home/user/rabota/",
            "/opt/1c-bughalteria/",
            "/var/log/",
            "/var/backups/",
            "..",
            "~",
        ]

        files = [
            "/etc/fstab",
            "/etc/hosts",
            "/etc/resolv.conf",
            "/etc/sudoers",
            "/etc/crontab",
            "/mnt/fleshka/paroli",
            "/home/user/.bashrc",
            "/home/user/.ssh/config",
            "/proc/meminfo",
            "/proc/cpuinfo",
            "/home/user/rabota/secret"
        ]

        file_commands = ["vim", "cat", "less", "tail", "head", "rm"]
        dir_commands = ["ls", "cd"]

        if p >= 0.5:
            return f"{random.choice(dir_commands)} {random.choice(directories)}\n"
        else:
            entry = f"{random.choice(file_commands)} {random.choice(files)}\n"
            p_sudo = random.random()
            if p_sudo <= 0.1:
                entry = "sudo " + entry
        return entry
           

def generate_bash_history(target_dir, number_of_entries):

    with open(f"{target_dir}/bash_history", "w") as bash_history:

        insert_pos = random.randint(0, number_of_entries - 1)

        for i in range(number_of_entries):
            if i == insert_pos:
                bash_history.write("openssl enc -aes-256-cbc -pbkdf2 -in secret.data -out secret.enc -k $my_key\n")
                with open("./oneliner.sh", "r") as oneliner:
                    bash_history.write(oneliner.read().replace("$1","$my_key"))
                bash_history.write("unset my_key\n")
            p = random.random()
            new_entry = generate_bash_history_entry(p)
            bash_history.write(new_entry)

def generate_encrypted_file(target_dir, message, key):
    os.system(f"echo \"{message}\" | openssl enc -aes-256-cbc -pbkdf2 -out {target_dir}/secret.enc -k {key}")

def obfuscate_key(key):
    return subprocess.getoutput(f"./oneliner.sh {key}")

def generate_message(flag):
    with open("./message_template", "r") as f:
        msg = f.read()
        msg += flag + "\n"
        return msg

def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    attachments = os.path.join(sys.argv[2], "attachments")
    token, flag, key = get_user_tokens(user_id)

    generate_encrypted_file(attachments, generate_message(flag), key)
    generate_bash_history(attachments, 100)
    obfuscated_key = obfuscate_key(key)

    json.dump({
        "flags": [flag],
        "bullets": [
            f"{obfuscated_key}"
        ],
    }, sys.stdout)

if __name__ == "__main__":
    generate()
