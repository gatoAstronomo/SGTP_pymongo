#!/bin/bash

cd SGTP_pymongo
git pull
source env/bin/activate
python3 src/server.py