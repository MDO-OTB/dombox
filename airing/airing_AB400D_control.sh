#!/bin/bash

# /dev/ttyUSB requires an user in the group dialout

WAIT_LOCK_DELAY=5
PICOCOM_ARGV='/dev/ttyUSB0 -b 57600 -qr  --omap crcrlf'
airing_lock() { 
  exec 200>/tmp/rflink_lock
  flock --no-fork --exclusive --wait ${WAIT_LOCK_DELAY}  200 || exit 3
  pid=$$
  echo $pid 1>&200
}

airing_config_opening() {
  AIRING_ID=$1
  echo 'opening' > /tmp/airing${AIRING_ID}
}

airing_config_opened() {
  AIRING_ID=$1
  echo 'opened' > /tmp/airing${AIRING_ID}
}

airing_config_closing() {
  AIRING_ID=$1
  echo 'closing' > /tmp/airing${AIRING_ID}
}

airing_config_closed() {
  AIRING_ID=$1
  echo 'closed' > /tmp/airing${AIRING_ID}
}

airing_start() {
  AIRING_ID=$1
  airing_config_opening ${AIRING_ID}
  echo "10;AB400D;60;${AIRING_ID};ON;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;AB400D;60;${AIRING_ID};ON;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;AB400D;60;${AIRING_ID};ON;" |picocom ${PICOCOM_ARGV}
  airing_config_opened ${AIRING_ID}
}

airing_stop() {
  AIRING_ID=$1
  airing_config_closing ${AIRING_ID}
  echo "10;AB400D;60;${AIRING_ID};OFF;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;AB400D;60;${AIRING_ID};OFF;" |picocom ${PICOCOM_ARGV}
  sleep 2
  echo "10;AB400D;60;${AIRING_ID};OFF;" |picocom ${PICOCOM_ARGV}
  airing_config_closed ${AIRING_ID}
}

case $1 in 
  start)
      airing_lock
      airing_start $2
      ;;
  stop)
      airing_lock
      airing_stop $2
      ;;
  *)
      exit -1
esac
