#!/usr/bin/env bash

if ! [[ -d /mnt/wslg ]]; then
  echo "$(tput setaf 1)"Can\'t find the wslg folder."$(tput sgr0)"
  echo "
You need to update windows 11 and wslg.
See more at: https://github.com/microsoft/wslg"
  exit 1
fi

{
  echo "DISPLAY=$DISPLAY
PULSE_SERVER=$PULSE_SERVER
WAYLAND_DISPLAY=$WAYLAND_DISPLAY
XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
} >.env
echo "$(tput setaf 2)"For WSLg: .env generated."$(tput sgr0)"

echo "------------------------ .env ----------------------------------"
cat .env
echo "----------------------------------------------------------------"

echo ""

cat ./docker/Docker-compose-wsl.yml >docker-compose.yml
echo "$(tput setaf 2)"For WSLg: Docker-compose.yml generated."$(tput sgr0)"

echo "------------------docker-compose.yml settings-------------------"
docker-compose config
echo "----------------------------------------------------------------"
