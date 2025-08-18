#!/bin/bash

FOLDERNAME='projects-rpi-setup-7'

echo
echo
echo "Welcome to the ENGR16X setup script!"
echo "This script will setup student accounts and appropriate settings."
echo

# we want to write these values to a file
# you can access these values in other scripts by doing
# source $INFOPATH
# and the variables will all be loaded in

INFOPATH="/home/pi/info.sh"
source $INFOPATH

echo ${TEAMNUMS[@]}
for account in ${TEAMNUMS[@]}
do
  echo
  echo "Adding $account account..."
  echo
  echo "Removing any existing Account Structure"
  sudo deluser $account
  sudo rm -r /home/$account
  echo "Creating $account account"
  sudo adduser $account --gecos "$account,0,0,0"
  echo "Changing $account account password"
  echo "$account:$account" | chpasswd
  echo "Adding reboot, shutdown, and poweroff sudo access"
  # echo "$instAcct ALL=(ALL) ALL" | sudo EDITOR='tee -a' visudo
  # echo "$instAcct ALL=NOPASSWD: /home/pi/Desktop/source_files/*" | sudo EDITOR='tee -a' visudo
  # echo "$instAcct ALL=NOPASSWD: /sbin/reboot, /sbin/shutdown, /sbin/poweroff" | sudo EDITOR='tee -a' visudo
  echo "$account ALL=NOPASSWD: /sbin/reboot, /sbin/shutdown, /sbin/poweroff" | sudo EDITOR='tee -a' visudo
  echo "$account ALL=NOPASSWD: /home/pi/Desktop/source_files/*" | sudo EDITOR='tee -a' visudo
  echo "$account ALL=NOPASSWD: /usr/bin/nmcli/*" | sudo EDITOR='tee -a' visudo
  echo "Creating Desktop"
  sudo mkdir /home/$account/Desktop
  sudo cp -r /home/pi/Desktop/new_desktop/. /home/$account/Desktop/
  echo "Adjusting Permissions"
  sudo chown -R $account:$account /home/$account/Desktop
  sudo chown -R pi:pi /home/$account/Desktop/"UPDATE FILES"
  sudo adduser $account i2c
  sudo adduser $account spi
  sudo adduser $account dialout
  sudo adduser $account gpio
  sudo adduser $account input
  sudo chown root:gpio /dev/mem
  sudo chmod g+rw /dev/mem
  sudo chmod -R 4755 /home/$account/Desktop/"UPDATE FILES"
  sudo /home/pi/$FOLDERNAME/setup_files/21_changeBackground.sh $account
  sudo cp -r /home/pi/.config/Thonny /home/$account/.config
  # sudo cp -r /home/pi/Desktop/source_files/. /home/$account/Desktop/source_files/
  sudo chmod 777 /home/$account/.config/Thonny/backend.log
  sudo chmod 777 /home/$account/.config/Thonny/frontend_faults.log
  sudo chmod 777 /home/$account/.config/Thonny/leave_this_empty
  sudo chmod 777 /home/$account/.config/Thonny/configuration.ini
  sudo chmod 777 /home/$account/.config/Thonny/frontend.log
done


echo
echo "Removing necessary file permissions"
sudo python3 /home/pi/$FOLDERNAME/setup_files/20_removePermissions.py

# might be causing errors
sudo raspi-config --expand-rootfs

cd ~

echo
echo
echo "Account Reset. This SD card is ready to be used by a team."
echo
