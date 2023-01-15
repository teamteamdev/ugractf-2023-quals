#!/usr/bin/env bash
set -e
tshark -r attachments/captured_traffic.pcap -Y http.response --export-objects http,extracted
convert extracted/hacker.jpg -crop x120+0+0 -threshold 10% - | tesseract - -
