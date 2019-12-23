from monitor import MonitorProducer
from monitor_utils import get_websites
from time import strftime
import sys
import time
import threading

chrono_running = True

def chrono():
    global chrono_running
    while chrono_running:
        sys.stdout.write(strftime('%M:%S'))
        sys.stdout.flush()
        sys.stdout.write("\b" * (100)) # return to start of line, after '['

        # print(time.time().strftime('%M:%S'))

thread = threading.Thread(target=chrono)
thread.start()


mon = MonitorProducer(delay=5, websites=get_websites('conf.txt'))
mon.start_monitoring()
print('start')
time.sleep(20)
mon.stop_monitoring()
print('stop')
time.sleep(5)
print('start again')
mon.start_monitoring()
time.sleep(10)
print('stop')
mon.stop_monitoring()

chrono_running = False
thread.join()
