#!/usr/bin/env bash

echo '2 checks:'

exit=`python3 --version`
[ $? != 0 ] && echo '[Error] Python3 not found' || echo '[OK] Python3 found'

exit=`mongod --version`
[ $? != 0 ] && echo '[Error] Mongodb not found' || echo '[OK] Mongodb found'