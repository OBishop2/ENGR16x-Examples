#!/bin/bash

# This checks to see if the team number was passed as an argument
# If it was not, it terminates the program
if [ -z "$1" ]
then
  echo
  echo "No team number was given. When using this file, a team number may be passed as the first argument as shown below."
  echo "sudo ./wifi_setup.sh team-number-goes-here"
  echo
  echo "Enter the team or kit number to be used for setup: "
  read teamNumber
  echo "Enter the Raspberry Pi Number: "
  read piNumber
else
  teamNumber=$1
  piNumber=1
fi

# This checks to see if the teamNumber is a number
# Any numeric value evaluation operation using non-numbers will result in an error, which is implicitly considered false in shell.
if [ "$teamNumber" -eq "$teamNumber" ]
then
  echo
  echo "Team/Kit number $teamNumber $piNumber will be used"
else
  echo "The Team/Kit number '$teamNumber $piNumber' is not valid"
  echo
  exit 1
fi

# now we check the number is between 1-255 inclusive
# as IPv4 only allows values in the range 0-255, and we dont have 0th teams
if [[ $teamNumber -lt 1 || $teamNumber -gt 255 ]]
then
    echo
    echo "The Team number $teamNumber is not valid."
    echo
    exit 1
fi

echo "Updating team number in all files"
sudo python3 ./updateTeamNumber.py $teamNumber $piNumber

echo "Stopping dnsmasq service before applying changes"
sudo systemctl disable dnsmasq
sudo systemctl stop dnsmasq

echo "Adding pi wifi connection"
sudo chmod +x ./addWifiConnection_kit.sh
sudo ./addWifiConnection_kit.sh

echo "Assign client ip addresses"
sudo python3 ./clientIp.py

echo "Splitting Wifi channel"
sudo chmod +x ./randomize_channel.sh
sudo ./randomize_channel.sh

echo "Configuring settings to accept ethernet internet connection"
echo "Setting IP forwarding"
sudo python3 ./IPForwarding.py

echo "Creating network translation between the ethernet port and the wifi drivers"
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

echo "Saving IP Table rules"
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

echo "Setting these rules in bootup"
sudo python3 rc.local.py

echo "Checking what's in the IP tables: "
sudo iptables -t nat -S
sudo iptables -S


echo "Starting pi wifi connection"
sudo chmod +x ./startWifiConnection.sh
sudo ./startWifiConnection.sh

# This may mess up the ethernet forwarding, commenting it out for now
# echo
# echo "Testing the Access Point now"
# echo "Testing hostapd"
# sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf


# these service [...] status pages need the user to enter q 
# to continue in the script. nobody knows that and it we 
# wrote to ctrl+c.....wow

#echo "Checking the running status"
#echo
#echo "HOSTAPD:"
#echo
#sudo service hostapd status
#echo
#echo "ISC-DHCP-SERVER:"
#echo
#sudo service dnsmasq status
#echo
#echo

# Might still need this?
# sudo update-rc.d hostapd enable

# we dont need this i think
#sudo update-rc.d isc-dhcp-server enable
#echo 
#echo

echo "Wifi Setup Complete"