#!/bin/bash

user_id="$2"
attachments="$3/attachments"

flag_suffix=$(echo "$user_id" | hmac256 "5z7cMW00ZXJKRg")
flag="ugra_r0tate_brack3ts_${flag_suffix:0:12}"
n=$(echo "$user_id" | md5sum | cut -c1-2)
n=$((0x${n%% *}))

printf "%s\n15) %s\n" "$(cat /text.txt)" "${flag}" > "${attachments}"/ciphered.txt
for i in $(seq 16 $n)
do
  echo "$i) $(/usr/games/fortune -s -n 80)" >> "${attachments}"/ciphered.txt
done

emacs --script /cipher.el --file "${attachments}"/ciphered.txt --eval "(cipher-buffer)"

echo "{\"flags\": [\"$flag\"]}"
