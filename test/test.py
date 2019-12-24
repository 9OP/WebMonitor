# from monitor import MonitorMaster
# from monitor_utils import get_websites
# from time import strftime
# import sys
# import time
# import threading

#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
from datetime import datetime

class MainWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="app")

		self.box = Gtk.Box(spacing=6)
		self.add(self.box)

		self.label = Gtk.Label()
		self.box.pack_start(self.label, True, True, 0)

	# Displays Timer
	def displayclock(self):
		#  putting our datetime into a var and setting our label to the result.
		#  we need to return "True" to ensure the timer continues to run, otherwise it will only run once.
		datetimenow = str(datetime.now().strftime('%H:%M:%S'))
		self.label.set_label(datetimenow)
		return True

	# Initialize Timer
	def startclocktimer(self):
		#  this takes 2 args: (how often to update in millisec, the method to run)
		GLib.timeout_add(1000, self.displayclock)



win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
win.startclocktimer()
Gtk.main()


#
#
#
#
#
#
#
# chrono_running = True
#
# def chrono():
#     global chrono_running
#     while chrono_running:
#         sys.stdout.write(strftime('%M:%S'))
#         sys.stdout.flush()
#         sys.stdout.write("\b" * (100))
#
# # thread = threading.Thread(target=chrono)
# # thread.start()
#
#
# # mon = MonitorProducer(delay=5, websites=get_websites('conf.txt'))
# # mon.start_producing()
# # print('start')
# # time.sleep(20)
# # mon.stop_producing()
# # print('stop')
# # time.sleep(5)
# # print('start again')
# # mon.start_producing()
# # time.sleep(10)
# # print('stop')
# # mon.stop_producing()
#
# mon = MonitorMaster(delay=5, websites=get_websites('websites.txt'))
# mon.start_monitoring()
# print('start')
# time.sleep(100)
# print('stop')
# mon.stop_monitoring()
# time.sleep(30)
# print('start again')
# mon.start_monitoring()
# time.sleep(10)
# print('final stop')
# mon.stop_monitoring()
#
# # chrono_running = False
# # thread.join()
