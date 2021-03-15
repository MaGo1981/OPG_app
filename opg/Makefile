SHELL := /bin/bash
.PHONY = usage

ROOT_DIR := $(shell pwd)

usage:
    @echo -e \
    "Usage :\n"\
    "make install      - install all needed packages on your system\n"\
    "make create_venv  - create new virtual environment in directory\n"\
    "make pypack       - install all needed packages needed to run opg_app\n"\


install:
    sudo apt install python3 python3-venv python3-pip virtualenv python3-virtualenv xvfb pyhton3-tk


create_venv:
    python3 -m venv env;
    @echo "Now run *source ./env/bin/activate* to activate your virtual env";

pypack:
    pip3 install -r requirements.txt