#!/usr/bin/env bash

# install virtualenv
check=`virtualenv --version`
[ $? != 0 ] && sudo pip3 install virtualenv

# check for virtualenv and datastore
[ -d "env" ] && python3 -m venv env
[ -d "env/db" ] && mkdir env/db

# activate virtualenv
source env/bin/activate

# install
pip3 install --upgrade pip
python3 setup.py build