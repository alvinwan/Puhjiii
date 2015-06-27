#!/usr/bin/env bash

# install virtualenv
check=`virtualenv --version`
[ $? != 0 ] && sudo pip3 install virtualenv

# check for virtualenv and datastore
python3 -m venv env
mkdir -p env/db

# activate virtualenv
source env/bin/activate

# install
pip3 install --upgrade pip
pip3 install -r requirements.txt

# run mongodb in background
mongod --dbpath env/db &

python3 setup.py build

mongo 127.0.0.1/admin --eval "db.shutdownServer()"
mongo 127.0.0.1/admin

echo "[OK] Installation complete."