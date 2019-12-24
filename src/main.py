from GUI import Interface, start_interface
from monitor import MonitorMaster
from monitor_utils import get_websites

import argparse


def arg():
    parser = argparse.ArgumentParser(description='DataDog take home web monitoring project')
    parser.add_argument('interval', type=int, help='check interval (seconds) in 2-10 minutes')
    args = parser.parse_args()
    return args


def main(check_interval, path='websites.txt'):
    # Backend and GUI instantiation
    mon = MonitorMaster(delay=check_interval, websites=get_websites(path))
    monGUI = Interface()

    # Connecting backend to GUI
    mon.connect_to_GUI(monGUI.update_monitoring)

    # Connecting GUI to backend
    monGUI.connect_to_monitor(mon.start_monitoring,
                              mon.stop_monitoring)

    # Start GUI
    start_interface(monGUI)

if __name__=='__main__':
    interval = arg().interval
    if interval>=120 and interval<=600:
        main(check_interval=interval)
    else:
        print('Interval must be between 120 and 600 seconds!')
        main(check_interval=5) # for debugging, remove before sending!!
