#!/bin/bash

# /dev/ttyUSB requires an user in the group dialout

WAIT_LOCK_DELAY=5
PICOCOM_ARGV='/dev/ttyUSB0 -b 57600 -qr  --omap crcrlf'
shutter_lock() { 
  exec 200>/tmp/rflink_lock
  flock --no-fork --exclusive --wait ${WAIT_LOCK_DELAY}  200 || exit 3
  pid=$$
  echo $pid 1>&200
}

shutter_config_opening() {
  SHUTTER_ID=$1
  echo 'opening' > /tmp/shutter${SHUTTER_ID}
}

shutter_config_opened() {
  SHUTTER_ID=$1
  echo 'opened' > /tmp/shutter${SHUTTER_ID}
}

shutter_config_closing() {
  SHUTTER_ID=$1
  echo 'closing' > /tmp/shutter${SHUTTER_ID}
}

shutter_config_closed() {
  SHUTTER_ID=$1
  echo 'closed' > /tmp/shutter${SHUTTER_ID}
}

shutter_open() {
  SHUTTER_ID=$1
  shutter_config_opening ${SHUTTER_ID}
  echo "10;RTS;${SHUTTER_ID};0;UP;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;UP;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;UP;" |picocom ${PICOCOM_ARGV}
  shutter_config_opened ${SHUTTER_ID}
}

shutter_close() {
  SHUTTER_ID=$1
  shutter_config_closing ${SHUTTER_ID}
  echo "10;RTS;${SHUTTER_ID};0;DOWN;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;DOWN;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;DOWN;" |picocom ${PICOCOM_ARGV}
  shutter_config_closed ${SHUTTER_ID}
}

shutter_stop() {
  SHUTTER_ID=$1
  shutter_config_closing ${SHUTTER_ID}
  echo "10;RTS;${SHUTTER_ID};0;STOP;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;STOP;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;RTS;${SHUTTER_ID};0;STOP;" |picocom ${PICOCOM_ARGV}
  shutter_config_closed ${SHUTTER_ID}
}

case $1 in 
  open)
      shutter_lock
      shutter_open $2
      ;;
  close)
      shutter_lock
      shutter_close $2
      ;;
  stop)
      shutter_lock
      shutter_stop $2
      ;;
  *)
      exit -1
esac
