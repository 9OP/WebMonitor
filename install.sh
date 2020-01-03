#!/bin/sh

# WebMonitor/  root path
BASEDIR="$( cd "$(dirname "$0")" ; pwd -P )"

# INSTALL GI LIB and other necessary stuff if not already installed
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 python3-pip

# INSTALL venv
pip3 install virtualenv

# CREATE VIRTUAL ENV (python3.3+)
python3 -m venv ${BASEDIR}/venv/

# INSTALL requirements for WebMonitor
${BASEDIR}/venv/bin/pip3 install -r ${BASEDIR}/resources/conf/requirements.txt

# ADD app to $PATH
PATH=$PATH:${BASEDIR}

echo "
[Desktop Entry]
Version=1.0
Name=WebMonitor
Icon=${BASEDIR}/resources/media/cctv.png
Exec=${BASEDIR}/webmonitor
Terminal=false
Type=Application
Categories=Utility;Application;
" > webmonitor.desktop

# ADD webmonitor.desktop to /usr/share/applications/
sudo cp ${BASEDIR}/webmonitor.desktop /usr/share/applications
