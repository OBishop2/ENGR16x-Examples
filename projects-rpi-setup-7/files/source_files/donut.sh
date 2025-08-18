#!/bin/bash

echo
echo "Downloading Files"

cd /home/pi/Desktop/updates/donut
git fetch --all
git reset --hard origin/master
git pull origin master

echo
echo "Applying Updates"
sudo chown -R pi:pi /home/pi/Desktop/updates/donut/donut
sudo chmod 711 /home/pi/Desktop/updates/donut/donut/run.sh
sudo /home/pi/Desktop/updates/donut/donut/run.sh
