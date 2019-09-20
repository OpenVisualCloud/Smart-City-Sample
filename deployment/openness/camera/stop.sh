#!/bin/bash -e

OFFICE=$(echo ${1-eee1} | cut -f4 -d'e')
sudo docker stack rm opncam
