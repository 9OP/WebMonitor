#!/bin/sh

# WebMonitor/  root path
BASEDIR=$(dirname "$0")

# INSTALL GI LIB and other necessary stuff if not already installed
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 python3-pip

# INSTALL venv
pip3 install venv

# CREATE VIRTUAL ENV
python3 -m venv ${BASEDIR}/venv/

# INSTALL requirements for WebMonitor
venv/bin/pip3 install -r ${BASEDIR}/resources/conf/requirements.txt

# ADD app to $PATH
PATH=$PATH:/home/siamang/Dev/WebMonitor/

# ADD webmonitor.desktop to /usr/share/applications/
sudo cp ${BASEDIR}/webmonitor.desktop /usr/share/applications
