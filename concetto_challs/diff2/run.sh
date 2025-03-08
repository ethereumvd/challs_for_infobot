#!/bin/sh

adduser -D $USER

echo $USER:$USER_PASSWORD | chpasswd

echo "FLAG='$FLAG'" > /root/secret.py

cp /root/chall.py /root/readme.txt /home/$USER

ssh-keygen -A

/usr/sbin/sshd

python3 /root/chall.py

