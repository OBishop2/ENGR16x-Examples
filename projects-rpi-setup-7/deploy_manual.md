# Steps to set up a new SD card for Student Use

Written by Nick Masso in May 2021.
Updated by Owen Bishop in August 2024.

The source of this file is at [https://github.com/engr16x/projects-rpi-setup-6/blob/main/deploy_manual.md](https://github.com/engr16x/projects-rpi-setup-6/blob/main/deploy_manual.md) and should be edited on github first, then changes propogated to the GDrive and Eagle.

## Pre-setup

Flash the sd card with the engr16x_v7.0 disk image. See the "Flashing an SD card" document. You do not have to decompress the `.gz` file for the imaging software to load the image correctly. 

## During setup

1.  insert the new SD card into the raspberrypi stack you want to set up

2.  connect the ethernet cable from the raspberrypi to your computer

3.  Power on the RPi

4.  SSH into the RPi with your client of choice. 
    
    From command prompt or terminal, the command is `ssh pi@engr.local`
    
    Using putty, the host name is `engr.local`
    
5.  Log in as the `pi` user. The password is `honors1234Admin`

    If the terminal says something about 
    
    ```
    The authenticity of host 'engr.local (fe80::bd18:7190:353e:e0ca%10)' can't be established.
    ECDSA key fingerprint is SHA256:ep88C0p1HafwD4Yoa7lnVTspSaYosj9M2x68YkNKQRc.
    Are you sure you want to continue connecting (yes/no)?
    ```
    
    type `yes` and press enter.

6.  Press the up arrow on your keyboard, this should show the command `sudo /home/pi/projects-rpi-setup-7/deploy.sh`

7.  Press enter to begin deploy.

8.  Follow the prompts on screen. Each time you are prompted for a password, simply press 'a' and then enter. This password will not be used by the pi and is simply needed for this step

9.  When complete, enter `sudo poweroff` to safely shut down the RPi. The green `act` light on the board should flash 10 times, and on the 10th flash should hold for a second and then turn off. This is how you know the RPi has completely powered down, and it is safe to unplug it.
