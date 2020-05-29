#!/bin/bash

APT_OK="no"
function check_apt() {
  if [ $APT_OK == "yes" ]; then
      return
  fi
 apt --version
  if [[ $? != 0 ]]; then
    echo "This script is currently only supported for linux  , which have the apt package manager"
    exit 1
  else
    APT_OK="yes"
  fi
}

echo "Checking apt, python3.8 and pip3.8"

PYTHON="python3.8"
PIP="$PYTHON -m pip"

$PYTHON -V
if [[ $? != 0 ]]; then
  check_apt
  sudo apt install $PYTHON python3-pip -y
fi
$PIP -V
if [[ $? != 0 ]]; then
  check_apt
  sudo apt install $PYTHON python3-pip -y
fi

echo "installing pip dependencies"

$PIP install -r requirements.txt

