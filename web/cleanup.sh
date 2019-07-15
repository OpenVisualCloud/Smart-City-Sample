#!/bin/bash

while true
do 
    find /var/www/thumbnail -type f -name "*.png" -mtime +1 -exec rm -f {} \;
    sleep 43200
done
