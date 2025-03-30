#! /bin/bash -x

set -e

while ! nc -z $BOOTSTRAP_SERVERS; do
  sleep 0.1
done

python src/main.py
