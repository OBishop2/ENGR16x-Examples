echo 0
sudo nmcli c delete pi_wifi
echo 1
sudo nmcli c add type wifi ifname wlan0 mode ap con-name pi_wifi ssid kit_REPLACEWITHTEAMNUMBER
echo 2
sudo nmcli c mod pi_wifi 802-11-wireless.band bg
echo 3
sudo nmcli c mod pi_wifi 802-11-wireless.channel 1
echo 4
sudo nmcli c mod pi_wifi 802-11-wireless-security.key-mgmt wpa-psk
echo 5
sudo nmcli c mod pi_wifi 802-11-wireless-security.proto rsn
echo 6
sudo nmcli c mod pi_wifi 802-11-wireless-security.group ccmp
echo 7
sudo nmcli c mod pi_wifi 802-11-wireless-security.psk raspberry
echo 8
sudo nmcli c mod pi_wifi ipv4.method shared
echo 9
sudo nmcli c mod pi_wifi ipv4.addresses 192.168.REPLACEWITHTEAMNUMBER.REPLACEWITHPINUMBER/24
echo 10
sudo nmcli c mod pi_wifi ipv6.method ignore