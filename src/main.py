from GUI import Interface, start_interface
from monitor import MonitorMaster
from monitor_utils import get_websites



def main():
    # Backend and GUI instantiation
    mon = MonitorMaster(delay=5, websites=get_websites('websites.txt'))
    monGUI = Interface()

    # Connecting backend to GUI
    mon.connect_to_GUI(monGUI.update_monitoring)

    # Connecting GUI to backend
    monGUI.connect_to_monitor(mon.start_monitoring,
                              mon.stop_monitoring)

    # Start GUI
    start_interface(monGUI)

if __name__=='__main__':
    main()