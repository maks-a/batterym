#!/bin/sh
set -e

python2 setup.py install --record install_log.txt --user "$@"
