#!/usr/bin/env bash
PREFIX="https://trisection.q.2023.ugractf.ru"
TOKEN="..."

part1="$(curl -D headers.txt -s "$PREFIX/$TOKEN/" | grep -Po "(?<=<!--).*?(?=-->)")"

part2_url="$(curl -s -L "$PREFIX/robots.txt" | grep -Po "(?<=Disallow: ).*")"
part2="$(curl -s "$PREFIX$part2_url")"

part3="$(grep -Po "(?<=flag_3: ).*" headers.txt)"

echo "$part1$part2$part3"
