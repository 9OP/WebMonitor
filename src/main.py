from GUI import Interface, start_interface
from monitor import MonitorMaster
from monitor_utils import get_websites

import argparse


def arg():
    parser = argparse.ArgumentParser(description='DataDog take home web monitoring project')
    parser.add_argument('--path', type=str, default='websites.txt',
                        help='path to websites.txt (http://example.com, 10)')
    args = parser.parse_args()
    return args


def main(path):
    # Backend and GUI instantiation
    delays, websites = get_websites(path)
    mon = MonitorMaster(delays=delays, websites=websites)
    monGUI = Interface()

    # Connecting backend to GUI
    mon.connect_to_GUI(monGUI.update_monitoring)

    # Connecting GUI to backend
    monGUI.connect_to_monitor(mon.start_monitoring,
                              mon.stop_monitoring)

    # Start GUI
    start_interface(monGUI)

if __name__=='__main__':
    path = arg().path
    main(path=path)
