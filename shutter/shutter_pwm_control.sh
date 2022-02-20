#!/bin/bash

#usefull link
#https://github.com/RobertCNelson/bb.org-overlays

#PWM   MOTOR   PWM PIN    CONTROLER BASE ADRESS     POLARITY PIN
#PWM1A 2       P9_14      48302200                  P8_16(gpio46)
#PWM1B 1       P9_16      48302200                  P8_18(gpio65)
#PWM2A 4       P9_14      48304200                  P8_26(gpio61)
#PWM1B 3       P9_16      48304200                  P8_14(gpio26)

SYS_OCP='/sys/devices/platform/ocp/'

#pwm detection : ls -l /sys/class/pwm

#pwm detected with Beagle bone black or Beagle bone black wifi and eMMC boot 
#pwm_motor1="${SYS_OCP}48302000.epwmss/48302200.pwm/pwm/pwmchip4/pwm-4:1"
#pwm_motor2="${SYS_OCP}48302000.epwmss/48302200.pwm/pwm/pwmchip4/pwm-4:0"
#pwm_motor3="${SYS_OCP}48304000.epwmss/48304200.pwm/pwm/pwmchip7/pwm-7:1"
#pwm_motor4="${SYS_OCP}48304000.epwmss/48304200.pwm/pwm/pwmchip7/pwm-7:0"

#pwm detected with Beagle bone black wifi  and sdcard boot
pwm_motor1="${SYS_OCP}48302000.epwmss/48302200.pwm/pwm/pwmchip0/pwm-0:1"
pwm_motor2="${SYS_OCP}48302000.epwmss/48302200.pwm/pwm/pwmchip0/pwm-0:0"
pwm_motor3="${SYS_OCP}48304000.epwmss/48304200.pwm/pwm/pwmchip2/pwm-2:1"
pwm_motor4="${SYS_OCP}48304000.epwmss/48304200.pwm/pwm/pwmchip2/pwm-2:0"

pwm_period=50000
#direction:out
#value 0|1
SYS_GPIO='/sys/class/gpio/'

polarity_motor1_gpio=65
polarity_motor2_gpio=46
polarity_motor3_gpio=26
polarity_motor4_gpio=61
polarity_motor1=${SYS_GPIO}gpio${polarity_motor1_gpio}/
polarity_motor2=${SYS_GPIO}gpio${polarity_motor2_gpio}/
polarity_motor3=${SYS_GPIO}gpio${polarity_motor3_gpio}/
polarity_motor4=${SYS_GPIO}gpio${polarity_motor4_gpio}/

OPEN_DELAY=30
CLOSE_DELAY=30

WAIT_LOCK_DELAY=32

export_gpio() {
  wait_gpio=0
  if ! test -e ${polarity_motor1}; then
    echo ${polarity_motor1_gpio} > /sys/class/gpio/export
    wait_gpio=1
  fi
  if ! test -e ${polarity_motor2}; then
    echo ${polarity_motor2_gpio} > /sys/class/gpio/export
    wait_gpio=1
  fi
  if ! test -e ${polarity_motor3}; then
    echo ${polarity_motor3_gpio} > /sys/class/gpio/export
    wait_gpio=1
  fi
  if ! test -e ${polarity_motor4}; then
    echo ${polarity_motor4_gpio} > /sys/class/gpio/export
    wait_gpio=1
  fi
  if test ${wait_gpio} -eq 1; then
    sleep 1
  fi
}

eval_pwm_path() {
  MOTOR_ID=$1
  case ${MOTOR_ID} in
    1)
      polarity_path=${polarity_motor1}
      pwm_path=${pwm_motor1}
      ;;
    2)
      polarity_path=${polarity_motor2}
      pwm_path=${pwm_motor2}

      ;;
    3)
      polarity_path=${polarity_motor3}
      pwm_path=${pwm_motor3}
      ;;
    4)
      polarity_path=${polarity_motor4}
      pwm_path=${pwm_motor4}
      ;;
    *)
      exit -1
  esac
}

init_pwm() {
  MOTOR_ID=$1
  eval_pwm_path $1
  echo 'out' > ${polarity_path}/direction
  echo '0' > ${polarity_path}/value
  echo ${pwm_period} > ${pwm_path}/period
  echo ${pwm_period} > ${pwm_path}/duty_cycle
  echo 0 > ${pwm_path}/enable
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
  eval_pwm_path ${SHUTTER_ID}
  init_pwm ${SHUTTER_ID}
  echo 1 > ${pwm_path}/enable
  sleep ${OPEN_DELAY}
  init_pwm ${SHUTTER_ID}
  shutter_config_opened ${SHUTTER_ID}
}

shutter_open_if() {
  SHUTTER_ID=$1
  status_file="/tmp/shutter${SHUTTER_ID}"
  shutter_status=''
  if test -f ${status_file}; then
    shutter_status=`cat ${status_file}`
  fi
  if [ "${shutter_status}" == "closed" ]; then
    shutter_open ${SHUTTER_ID}
  fi
}

shutter_close() {
  SHUTTER_ID=$1
  shutter_config_closing ${SHUTTER_ID}
  eval_pwm_path ${SHUTTER_ID}
  init_pwm ${SHUTTER_ID}
  echo 1 > ${polarity_path}/value
  echo 1 > ${pwm_path}/enable
  sleep ${CLOSE_DELAY}
  init_pwm ${SHUTTER_ID}
  shutter_config_closed ${SHUTTER_ID}
}

shutter_close_if() {
  SHUTTER_ID=$1
  status_file="/tmp/shutter${SHUTTER_ID}"
  shutter_status=''
  if test -f ${status_file}; then
    shutter_status=`cat ${status_file}`
  fi
  if [ "${shutter_status}" == "opened" ]; then
    shutter_close ${SHUTTER_ID}
  fi
}

shutter_stop() {
  SHUTTER_ID=$1
  eval_pwm_path $1
  init_pwm ${SHUTTER_ID}
  rm /tmp/shutter_pwm_lock
  pkill -15 shutter_pwm_control
}


shutter_lock() { 
  exec 200>/tmp/shutter_pwm_lock
  flock --no-fork --exclusive --wait ${WAIT_LOCK_DELAY}  200 || exit 3
  pid=$$
  echo $pid 1>&200
}

export_gpio

case $1 in 
  force_open)
      shutter_lock
      shutter_open $2
      ;;
  open)
      shutter_lock
      shutter_open_if $2
      ;;
  force_close)
      shutter_lock
      shutter_close $2
      ;;
  close)
      shutter_lock
      shutter_close_if $2
      ;;
  stop)
      shutter_stop $2
      ;;
  *)
      exit -1
esac
