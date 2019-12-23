from scheduler import Scheduler
from database import Database
from monitor_utils import _monitor_website, _monitor_dump

class MonitorProducer:
    ''' Monitor websites and dump results into project database
        Produce raw monitoring data.
    :param delay: check intervals for monitoring in seconds
    :param websites: list of website (http addresses) to monitor
    '''

    def __init__(self, delay, websites):
        self.delay = delay
        self.websites = websites
        self.sched = []

    @staticmethod
    def _monitor(website):
        ''' Static method (usable without class instance)
            Collect monitoring data from website and dump it
            into project database
        :param website: website to monitor
        '''
        data = _monitor_website(website)
        _monitor_dump(data)

    def start_monitoring(self):
        ''' Start monitoring process...
            Create Scheduler for each websites
        '''
        for website in self.websites:
            sched = Scheduler(self.delay, self._monitor, website)
            sched.start()
            self.sched.append(sched)

    def stop_monitoring(self):
        ''' Stop monitoring process...
            Cancel every known Schedulers
        '''
        for sched in self.sched:
            sched.stop()



class MonitorConsumer:
    ''' Consume data from project database
        Calculate and output interresting metrics (rate of availability,
        average response time, status code rate)
    '''

    def __init__(self):
        pass
