from scheduler import Scheduler
from database import Database
from monitor_utils import _monitor_website, _monitor_dump, _monitor_collect, _metrics_print



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
            Monitor data from website and dump it
            into project database
        :param website: website to monitor
        '''
        data = _monitor_website(website)
        _monitor_dump(data)

    def start_producing(self):
        ''' Start producing process...
            Create Scheduler for each websites
        '''
        for website in self.websites:
            sched = Scheduler(self.delay, self._monitor, website)
            sched.start()
            self.sched.append(sched)

    def stop_producing(self):
        ''' Stop producing process...
            Cancel every known Schedulers
        '''
        for sched in self.sched:
            sched.stop()



class MonitorConsumer:
    ''' Consume data from project database
        Calculate and output interresting metrics (rate of availability,
        average response time, status code rate)
    :param websites: list of websites (http addresses)
    '''

    def __init__(self, websites):
        self.websites = websites
        self.sched = []

    # @staticmethod
    def _collector(self, interval, website):
        ''' Collect data from project database
            and compute metrics.
        :param interval: look back interval (in seconds)
        :param website: website http addresse
        '''
        metrics = _monitor_collect(interval, website)
        if interval==600: #10minutes
            self.send_to_GUI(metrics=metrics, mon='10min')
        elif interval==3600: #1hour
            self.send_to_GUI(metrics=metrics, mon='1hour')

        # _metrics_print(website, interval, metrics) #for debugging

    def start_consuming(self):
        ''' Start consuming process...
            Create Scheduler for each websites
        '''
        for website in self.websites:
            # Check interval: 120 seconds, for the last 600 seconds
            # sched_10min = Scheduler(2*60, self._collector, 10*60, website)
            # Check interval: 600 seconds, for the last 3600 seconds
            # sched_1hour = Scheduler(10*60, self._collector, 60*60, website)
            sched_10min = Scheduler(10, self._collector, 10*60, website)
            sched_1hour = Scheduler(20, self._collector, 60*60, website)
            sched_10min.start()
            sched_1hour.start()
            self.sched.append(sched_10min)
            self.sched.append(sched_1hour)

    def stop_consuming(self):
        ''' Stop consuming process...
            Cancel every known Schedulers
        '''
        for sched in self.sched:
            sched.stop()

    @staticmethod
    def send_to_GUI(**kwargs):
        # override with GUI update_monitoring
        pass



class MonitorMaster:
    def __init__(self, delay, websites):
        self._producer = MonitorProducer(delay, websites)
        self._consumer = MonitorConsumer(websites)

    def start_monitoring(self):
        self._producer.start_producing()
        self._consumer.start_consuming()

    def stop_monitoring(self):
        self._producer.stop_producing()
        self._consumer.stop_consuming()

    def connect_to_GUI(self, function):
        self._consumer.send_to_GUI = function
