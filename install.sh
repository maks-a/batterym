#!/bin/sh
set -e

python setup.py install --record install_log.txt --user "$@"
