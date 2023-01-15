#!/usr/bin/env bash
set -e

KEY="..."

my_key=$(
	<<<"$KEY" \
		awk '{print substr($0,length/2+1) substr($0,1,length/2)}' | \
		xargs -I {} python3 -c "import sys;print(f'{int(sys.argv[1],16)^int((sys.argv[2]*(len(sys.argv[1])//len(sys.argv[2])+1))[:len(sys.argv[1])],16):34x}')" {} deadbeef | \
		xxd -r -p | \
		rev | \
		tr '[N-ZA-Mn-za-m3-90-2]' '[A-Za-z0-9]' | \
		base64 -d
)

openssl enc -d -aes-256-cbc -pbkdf2 -in attachments/secret.enc -out - -k "$my_key" | tail -2
