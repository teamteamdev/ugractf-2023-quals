#!/usr/bin/env nix-shell
#!nix-shell -p docker-compose -p tcpreplay -p gnugrep -p gawk -i bash

set -e

# argument processing
export FLAG="$1"
workdir="$2"

# setting work directory and creating tmp dir
gendir="$(dirname "${BASH_SOURCE[0]}")"
cd $gendir

# generate suffix & project name
suffix="$(tr -dc a-z0-9 </dev/urandom 2>/dev/null | head -c 16)"
export COMPOSE_PROJECT_NAME=capture_$suffix

# docker start
docker-compose up -d --build >&2
trap "docker-compose down -t 1 >&2" INT TERM EXIT
docker-compose logs -f >&2 &

# waiting for client to finish or exit with timeout
status() { docker-compose ps --services --filter status=running; }

success=
for i in `seq 1 20`; do
  if [[ "$(status)" != *"client"* ]]; then
    success=1
    break
  fi
  sleep 1
done

if [ -z "$success" ]; then
  echo "Timeout" >&2
  exit 1
fi

# fix checksum in captured traffic
tcprewrite --fixcsum --infile $TMPDIR/capture.pcap --outfile=$workdir/captured_traffic.pcap
