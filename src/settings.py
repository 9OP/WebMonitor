import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASEDIR = os.path.dirname(SRC_DIR)
# BASEDIR = /path/to/WebMonitor/
sys.path.append(BASEDIR) # add WebMonitor path to pythonpath
