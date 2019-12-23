from scheduler import Scheduler
from database import Database
from monitor_utils import _monitor_website, _monitor_dump

class MonitorProducer:

    def __init__(self, delay, websites):
        self.delay = delay
        self.websites = websites
        self.sched = []

    @staticmethod
    def _monitor(website):
        data = _monitor_website(website)
        _monitor_dump(data)

    def start_monitoring(self):
        for website in self.websites:
            sched = Scheduler(self.delay, self._monitor, website)
            sched.start()
            self.sched.append(sched)

    def stop_monitoring(self):
        for sched in self.sched:
            sched.stop()
