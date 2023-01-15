#!/usr/bin/env sh
mkdir -p /state/dbs
exec gunicorn -b unix:/tmp/app.sock 'server:make_app("/state")'
