#!/usr/bin/env bash

mkdir ~/.virtualenv
cd ~/.virtualenv/
python3.5 -m venv magic
source ./magic/bin/activate
pip install -r requirements.txt
