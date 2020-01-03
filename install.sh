#!/bin/sh

# CREATE VIRTUAL ENV
python3 -m venv venv/
# INSTALL GI LIB and other necessary stuff if not already installed
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
# INSTALL requirements for WebMonitor
venv/bin/pip3 install -r requirements.txt
