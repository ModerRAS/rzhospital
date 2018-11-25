#!/bin/bash
python3 RZ_hospital_Spider.py
python3 AutoGit.py
sleep 1m
./rzhs.sh &
