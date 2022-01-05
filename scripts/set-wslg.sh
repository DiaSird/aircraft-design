#!/usr/bin/env bash

if ! [[ -d /mnt/wslg ]]; then
  echo "$(tput setaf 1)"Can\'t find the wslg folder."$(tput sgr0)"
  echo "
You need to update windows 11 and wslg.
See more at: https://github.com/microsoft/wslg"
  exit 1
fi

wslgDir="./docker/wslg"
envPath="$wslgDir/.env.wslg"

{
  echo "DISPLAY=$DISPLAY
PULSE_SERVER=$PULSE_SERVER
WAYLAND_DISPLAY=$WAYLAND_DISPLAY
XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
} >$envPath
echo "$(tput setaf 2)"For WSLg: .env generated."$(tput sgr0)"

echo "------------------------ $envPath -------------------------"
cat $envPath
echo "----------------------------------------------------------------"

echo ""

cat "$wslgDir"/Docker-compose-wslg.yml >docker-compose.yml
echo "$(tput setaf 2)"For WSLg: Docker-compose.yml generated."$(tput sgr0)"

echo "------------------docker-compose.yml settings-------------------"
docker-compose config
echo "----------------------------------------------------------------"
