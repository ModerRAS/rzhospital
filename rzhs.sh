#!/bin/bash
python3 RZ_hospital_Spider.py
chown -R www-data:www-data /var/www/html/rzhpt.xml
sleep 1m
./rzhs.sh &
