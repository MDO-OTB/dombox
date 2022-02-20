#!/bin/sh
#pip3 install netifaces
#pip3 install flup
#pip3 install urlparse
#pip3 install schedule
#pip3 install wheel
#pip3 install Adafruit-DHT
service dombox_agent stop
service lighttpd stop
tar  xvf ${1} --no-same-owner --no-same-permissions -C /
chown -R www-data:www-data /var/www/*
chmod 755 /var/www/*
chmod 644 /etc/lighttpd/lighttpd.conf
chmod 755 /etc/lighttpd
chmod 755 /etc/init.d/dombox_agent
chmod 755 /usr/bin/dombox_agent.py
chmod 755 /usr/bin/shutter_rts_control.sh
chmod 755 /usr/bin/shutter_pwm_control.sh
chmod 755 /usr/bin/airing_AB400D_control.sh
chmod 755 /usr/bin/alarm_AB400D_control.sh
SHUTTER_ID='1 2 FFFFA0 FFFFB0 FFFFC0 FFFFD0 FFFFF0'
for id  in "${SHUTTER_ID}"; do
  if [ -f "/tmp/shutter${id}" ]; then
    chmod 644 /tmp/shutter${id}
    chmod www-data:www-data /tmp/shutter${id}
  fi
done
touch /etc/domConfig
chown www-data:www-data /etc/domConfig 
chmod 644 /etc/domConfig 
systemctl enable dombox_agent
timedatectl set-timezone Europe/Paris
service dombox_agent start
service lighttpd start
addgroup www-data gpio
addgroup www-data dialout
