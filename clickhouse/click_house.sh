#! /bin/bash -x

# set -e
# export BOOTSTRAP_SERVERS=127.0.0.1:10000
# while ! nc -z $BOOTSTRAP_SERVERS; do
#   sleep 2
# done

python src/main.py
