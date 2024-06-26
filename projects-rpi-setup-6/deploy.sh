#!/bin/bash

hostname="engr"
instAcct="instructor"
FOLDERNAME='projects-rpi-setup-6'
setup_path="/home/pi/$FOLDERNAME/setup_files/wifi_setup"

echo
echo
echo "Welcome to the ENGR16X setup script!"
echo "This script will setup student accounts and appropriate settings."
echo
echo

echo
echo "Is this a team kit or a minikit? (enter 't' or 'm')"
read TYPE

# declares an empty list array
TEAMNUMS=()
if [ $TYPE == "t" ]
then
  echo "Enter the team number (1-255):"
  read tNum
  team="team_$tNum"
  TEAMNUMS+=($team)

  echo "Enter the pi number:"
  read PINUM
  
elif [ $TYPE == "m" ]
then
  echo "Enter the kit number:"
  read tNum

  echo "Enter the account names to set up (traditionally section_X):"
  read acct
  while [ "$acct" != "" ]
  do
    TEAMNUMS+=($acct)
    echo "Enter the account names to set up: (Press [Enter] if all are entered"
    read acct
  done
  PINUM=1
  
else
  echo "Invalid Entry"
  exit
fi



# we want to write these values to a file
# you can access these values in other scripts by doing
# source $INFOPATH
# and the variables will all be loaded in

INFOPATH="/home/pi/info.sh"
echo "" >> $INFOPATH
echo "#!/bin/bash" >> $INFOPATH
echo "TEAMNUMS=(${TEAMNUMS[*]})" >> $INFOPATH
echo "PINUM=$PINUM" >> $INFOPATH
# for our own analysis, lets write the current date.
SETUPDATE=`date`
echo "SETUPDATE=$SETUPDATE" >> $INFOPATH

echo "Changing password of default user 'pi'"
echo "pi:honors1234Admin" | chpasswd

cd $setup_path
echo
echo "Creating TA Account"
echo
echo "Removing any existing Account Structure"
sudo deluser $instAcct
echo "Creating instructor account: $instAcct"
sudo adduser $instAcct --disabled-login --gecos "$instAcct,0,0,0"
echo "Changing $instAcct account password..."
echo "$instAcct:honors1234" | chpasswd
echo "Adding sudo access"
echo "$instAcct ALL=(ALL) ALL" | sudo EDITOR='tee -a' visudo
echo "$instAcct ALL=NOPASSWD: /home/pi/Desktop/source_files/*" | sudo EDITOR='tee -a' visudo
echo "$instAcct ALL=NOPASSWD: /sbin/reboot, /sbin/shutdown, /sbin/poweroff" | sudo EDITOR='tee -a' visudo
echo "Creating Desktop"
sudo mkdir /home/$instAcct/Desktop
sudo cp -r /home/pi/Desktop/new_desktop/. /home/$instAcct/Desktop/
echo "Adjusting Permissions"
sudo chown -R $instAcct:$instAcct /home/instructor/Desktop
sudo adduser $instAcct i2c
sudo adduser $instAcct spi
sudo adduser $instAcct gpio
sudo adduser $instAcct input
sudo chown root.gpio /dev/mem
sudo chmod g+rw /dev/mem
sudo chmod -R 4777 /home/$instAcct/Desktop/"UPDATE FILES"
sudo /home/pi/$FOLDERNAME/setup_files/21_changeBackground.sh $instAcct



for account in ${TEAMNUMS[@]}
do
  echo
  echo "Adding $account account..."
  echo
  echo "Removing any existing Account Structure"
  sudo deluser $account
  sudo rm -r /home/$account
  echo "Creating $account account"
  sudo adduser $account --disabled-login --gecos "$account,0,0,0"
  echo "Changing $account account password"
  echo "$account:$account" | chpasswd
  echo "Adding reboot, shutdown, and poweroff sudo access"
  echo "$account ALL=NOPASSWD: /sbin/reboot, /sbin/shutdown, /sbin/poweroff" | sudo EDITOR='tee -a' visudo
  echo "$account ALL=NOPASSWD: /home/pi/Desktop/source_files/*" | sudo EDITOR='tee -a' visudo
  echo "Creating Desktop"
  sudo mkdir /home/$account/Desktop
  sudo cp -r /home/pi/Desktop/new_desktop/. /home/$account/Desktop/
  echo "Adjusting Permissions"
  sudo chown -R $account:$account /home/$account/Desktop
  sudo chown -R pi:pi /home/$account/Desktop/"UPDATE FILES"
  sudo adduser $account i2c
  sudo adduser $account spi
  sudo adduser $account gpio
  sudo adduser $account input
  sudo chown root.gpio /dev/mem
  sudo chmod g+rw /dev/mem
  sudo chmod -R 4755 /home/$account/Desktop/"UPDATE FILES"
  sudo /home/pi/$FOLDERNAME/setup_files/21_changeBackground.sh $account
done


echo
echo "Removing necessary file permissions"
sudo python3 /home/pi/$FOLDERNAME/setup_files/20_removePermissions.py

sudo raspi-config --expand-rootfs


echo
echo "Beginning Wifi setup"
echo

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

cd $setup_path
sudo chmod 755 ./engr16x_wifi_setup.sh

echo
echo "Setting up team $tNum pi $PINUM"
sudo $setup_path/engr16x_wifi_setup.sh $tNum $PINUM


cd ~

echo
echo
echo "Deploy Complete. This SD card is ready to be used by a team."
echo