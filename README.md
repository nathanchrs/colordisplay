Raspbian Lite

- Download image
- On other computer, burn the image using Etcher
- Enable SSH: create file with name ssh in sdcard boot partition
- Insert card to Pi, turn on, connect to wired network
- From the same network, ssh pi@raspberrypi.local, password: raspberry (use PuTTY on windows)

/*[
	- Change default password: passwd
	Enter old password: raspberry
	Enter new password: passwordpi
	Confirm new password

	- Change hostname
	(For editing files, use nano: nano <filename>, Ctrl+o to save, Ctrl+x to exit)
	Edit /etc/hosts (use sudo), change 127.0.1.1 raspberrypi entry to new hostname (leddisplay)
	Edit /etc/hostname (use sudo), change contents to new hostname (leddisplay)

	- Expand fs
	- sudo apt update && sudo apt-get upgrade
	- Change timezone
	- Enable serial
]*/

[
	or just use sudo raspi-config:
	(Arrows to select dropdown, tab to change focus, space to check checkboxes, enter to click)
	- Update tool (optional)
	- Advanced - expand filesystem (optional)
	- Change hostname: <newhostname> (e.g. leddisplay)
	- Change password: <newpassword> (e.g. passwordpi)
	- Change timezone
	- Enable serial: login shell over serial NO, serial hardware interface YES
]

- Set up Wifi, need Internet: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
Summary:
- Scan networks: sudo iwlist wlan0 scan
- Config file: /etc/wpa_supplicant/wpa_supplicant.conf
- Append:
For secure networks:

network={
    ssid="testing"
    psk="testingPassword"
}

For open networks:

network={
    ssid="testing"
    key_mgmt=NONE
}

For hidden networks:

network={
    ssid="yourHiddenSSID"
    scan_ssid=1
    psk="Your_wifi_password"
}

Check using ifconfig, there should be inet addr in wlan0 section if connected. May need to reboot first or disconnect wired first.

- Reboot: sudo reboot
- ssh again, now using ssh pi@<newhostname>.local, password: <newpassword>
ssh pi@leddisplay.local, password: passwordpi

- Ensure pi user is part of dialout group (serial permission, use `groups pi`), if not, add to group `useradd -G dialout pi`, then reboot
- Connect serial wires (WARNING: 3.3V inputs only, use adapter if not)
- Install git to ease deployment `sudo apt install git`
- Install pip: sudo apt install python-pip python-dev python-virtualenv lighttpd
- Use SFTP or Git to copy files (e.g. with filezilla, host: <newhostname>.local, port: default (22), password: <newpassword>)
- Install app
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux-even-on-the-raspberry-pi
- Set up app config if needed

- Test app, web config


