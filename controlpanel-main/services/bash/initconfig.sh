#!/bin/bash
# Privo di inizializzazione interfacce eth0, eth1 e delle righe per l'autostart degli eseguibili
sudo update-initramfs -u
sudo systemctl enable systemd-networkd.service
sudo apt-get -y install avrdude
sudo apt-get -y install xscreensaver
sudo apt-get -y install pure-ftpd
sudo groupadd ftpgroup
sudo useradd ftpuser -g ftpgroup -s /sbin/nologin -d /dev/null
sudo mkdir /home/pi/FTP
sudo chown -R ftpuser:ftpgroup /home/pi/FTP
sudo pure-pw useradd upload -u ftpuser -g ftpgroup -d /home/pi/FTP -m
sudo pure-pw mkdb
sudo ln -s /etc/pure-ftpd/conf/PureDB /etc/pure-ftpd/auth/60puredb
echo "yes" | sudo tee /etc/pure-ftpd/conf/ChrootEveryone
echo "yes" | sudo tee /etc/pure-ftpd/conf/NoAnonymous
echo "yes" | sudo tee /etc/pure-ftpd/conf/AnonymousCantUpload
echo "no" | sudo tee /etc/pure-ftpd/conf/AnonymousCanCreateDirs
echo "no" | sudo tee /etc/pure-ftpd/conf/DisplayDotFiles
echo "yes" | sudo tee /etc/pure-ftpd/conf/DontResolve
echo "yes" | sudo tee /etc/pure-ftpd/conf/ProhibitDotFilesRead
echo "yes" | sudo tee /etc/pure-ftpd/conf/ProhibitDotFilesWrite
sudo service pure-ftpd restart
sudo apt-get update -y
sudo apt-get -y install apache2 -y
sudo service apache2 start
sudo apt-get -y install mariadb-server
sudo service apache2 restart
sudo mysql -u root
sudo pip3 install mysql.connector
sudo pip3 install pymodbus
sudo pip3 install numpy
sudo apt-get -y install python3-pyqt5
sudo pip3 install evdev
sudo pip3 install evasdk
sudo pip3 install qled
sudo apt-get -y install python3-pyqt5.qtsvg
sudo pip3 install matplotlib
#sudo pip3 install pyquaternion
sudo apt-get -y install libatlas-base-dev
sudo service mysql restart




