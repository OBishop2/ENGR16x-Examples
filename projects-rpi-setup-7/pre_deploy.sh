#!/bin/bash

CALLDIR=`pwd`
# this should be /home/pi/$FOLDERNAME unless someone updates the name of the repository
# notice that this requires you cd into this directory before running pre_deploy
FOLDERNAME='projects-rpi-setup-7'
HOSTNAME="engr"

# making deploy executable
sudo chmod 755 ./deploy.sh
sudo chmod 755 ./clear_account.sh

echo "Apt updating and upgrading"
sudo apt-get update --allow-releaseinfo-change-suite
sudo apt-get upgrade -y

echo "Installing and uninstalling requirements"
# Generic dependencies
sudo apt-get install samba libncurses5 default-jdk xrdp dnsmasq hostapd libffi-dev libatlas-base-dev pcmanfm -y

#IPTables for network things
sudo apt-get install iptables -y

# stuff that is in the grove.py deb dependencies
sudo apt-get install --no-install-recommends -y git libi2c-dev i2c-tools  \
    python3-setuptools python3-pip python3-smbus python3-dev python3-serial python3-rpi.gpio python3-numpy python3-scipy

# install more python libraries because they deserve it :)
echo "1"
echo "1"
echo "1"
echo "1"
echo "1"
echo "1"
# install more python libraries because they deserve it :)
sudo apt install python3-numpy
echo "2"
echo "2"
echo "2"
echo "2"
echo "2"
echo "2"
sudo apt install python3-matplotlib -y
echo "3"
echo "3"
echo "3"
echo "3"
echo "3"
sudo apt install python3-pandas -y
echo "4"
echo "4"
echo "4"
echo "4"
sudo apt install python3-scipy -y

echo "5"
echo "5"
echo "5"
echo "5"

# remove geany so thonny is the default editor
sudo apt-get purge geany -y
sudo apt autoremove -y

# install grove.py library for BaseHAT
# clone the repository (copy the code to the Pi)
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
# build the code from the repository
sudo pip3 install . --break-system-packages
cd /home/pi

git clone https://github.com/engr16x/python-build-hat.git
cd python-build-hat
sudo pip3 install . --break-system-packages
cd /home/pi

# install dependencies for the IMU
git clone https://github.com/turmary/bmi088-python.git
cd bmi088-python
git submodule init
git submodule update
make install
sudo cp libakicm.so /lib
cd ..

# remove unecessary directories (folders)
rm -rf bmi088-python 

# update Pi libraries
sudo apt update

echo "Changing raspi-config settings"
# dont autologin to gui
sudo raspi-config nonint do_boot_behaviour B1
# enable comms stuff (0 is enable)
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_serial_cons 1
sudo raspi-config nonint do_serial_hw 0

# set wifi country 
sudo raspi-config nonint do_wifi_country "US"
# set locale
sudo raspi-config nonint do_change_locale "en_US.UTF-8"
LANG="en_US.UTF-8"
sudo dpkg-reconfigure -f noninteractive locales
sudo raspi-config nonint do_change_timezone "America/New_York"
# keyboard fails. idk why
#sudo raspi-config nonint do_configure_keyboard "US"


echo "Modifying hardware permissions"
cd $CALLDIR/setup_files
sudo python3 01_config.py
sudo python3 01_modules.py
sudo python3 01_raspi-blacklist.py
echo "Modifiying Update Permission"
sudo python3 01_allow_update.py
echo "Modifying Wifi Permission"
sudo python3 01_allow_wifi_scan.py


echo "Changing XRDP settings"
sudo cp $CALLDIR/files/resources/loginLogo.bmp /usr/share/xrdp/logo.bmp
sudo cp $CALLDIR/files/resources/loginBackground.bmp /usr/share/xrdp/background.bmp
sudo cp $CALLDIR/files/resources/xrdp.ini /etc/xrdp/xrdp.ini

# Fixes issues with connecting via Remote Desktop Connection
sudo sed -i 's#exec systemd-inhibit --what=handle-power-key /usr/bin/lxsession -s LXDE-pi -e LXDE#exec /usr/bin/lxsession -s LXDE-pi -e LXDE#g' /usr/bin/startlxde-pi

cd $CALLDIR

echo "Copying credits.txt to a better location"
cp ./files/credits.txt /home/pi/credits.txt

cd $CALLDIR/setup_files

echo
echo "Default python version is: "
python --version
echo "It should be 3.11 or greater"

echo
echo

echo "Copying newdesktop directory to pi desktop"
cp -r $CALLDIR/files/new_desktop/. /home/pi/Desktop/new_desktop/

cd /home/pi/
# clone the Examples repository (copy the code)
# git clone https://github.com/engr16x/ENGR16x-Examples.git
git clone --depth 1 https://github.com/engr16x/ENGR16x-Examples.git

mkdir /home/pi/Desktop/new_desktop/Examples
# copy examples to the desktop
cp -r /home/pi/ENGR16x-Examples/Examples/. /home/pi/Desktop/new_desktop/Examples
# copy source files to Desktop
mkdir /home/pi/Desktop/new_desktop/basehat
cp -r /home/pi/ENGR16x-Examples/basehat/. /home/pi/Desktop/new_desktop/basehat
mkdir /home/pi/Desktop/new_desktop/buildhat
cp -r /home/pi/ENGR16x-Examples/buildhat/. /home/pi/Desktop/new_desktop/buildhat
cp -r $CALLDIR/files/source_files/. /home/pi/Desktop/source_files/

# copy all of the classes to PATH so that from basebat import * can be used
sudo cp /home/pi/ENGR16x-Examples/basehat.py /usr/local/lib/python3.11/dist-packages/basehat.py

# remove unecessary directories
rm -rf ENGR16x-Examples

echo
echo "Setting up file structure to sync with github update repositories"

mkdir /home/pi/Desktop/updates
cd /home/pi/Desktop/updates

echo "Setting up Thonny"
sudo cp -r /home/pi/$FOLDERNAME/Thonny /home/pi/.config/Thonny
sudo chmod 777 /home/pi/.config/Thonny/backend.log
sudo chmod 777 /home/pi/.config/Thonny/frontend_faults.log
sudo chmod 777 /home/pi/.config/Thonny/leave_this_empty
sudo chmod 777 /home/pi/.config/Thonny/configuration.ini
sudo chmod 777 /home/pi/.config/Thonny/frontend.log

echo
echo "Setting up projects-updates/boat"
sudo rm -r boat
mkdir boat
cd boat
git init
git config core.sparsecheckout true
echo boat/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/design-challenge"
sudo rm -r design-challenge
mkdir design-challenge
cd design-challenge
git init
git config core.sparsecheckout true
echo design-challenge/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/donut"
sudo rm -r donut
mkdir donut
cd donut
git init
git config core.sparsecheckout true
echo donut/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/duck"
sudo rm -r duck
mkdir duck
cd duck
git init
git config core.sparsecheckout true
echo duck/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/elephant"
sudo rm -r elephant
mkdir elephant
cd elephant
git init
git config core.sparsecheckout true
echo elephant/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/in-class-activities"
sudo rm -r in-class-activities
mkdir in-class-activities
cd in-class-activities
git init
git config core.sparsecheckout true
echo in-class-activities/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/plane"
sudo rm -r plane
mkdir plane
cd plane
git init
git config core.sparsecheckout true
echo plane/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

echo
echo "Setting up projects-updates/projects"
sudo rm -r projects
mkdir projects
cd projects
git init
git config core.sparsecheckout true
echo projects/ >> .git/info/sparse-checkout
git remote add -f origin https://github.com/engr16x/projects-updates.git
git pull origin master
cd ..

cd $CALLDIR/setup_files

echo "Making the desktop bg change script executable"
sudo chmod 755 ./21_changeBackground.sh

echo "Making source files executable"
python3 ./03_makeSourceFilesExecutable.py

cd $CALLDIR/setup_files

echo "Changing hostname to $HOSTNAME"
echo "Make sure hostname is set to default before this script is run:"
echo "raspberrypi"
sudo python3 ./05_changeHostname.py $HOSTNAME


echo "Copying modified user-facing files"
sudo cp ./06_bash_hist.txt /home/pi/.bash_history
sudo cp ./07_motd.txt /etc/motd

echo
echo "Pre-deploy setup is now complete. You may power off and image this disk."
