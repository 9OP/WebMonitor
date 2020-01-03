import unittest
import sys
import os
sys.path.append('./src/')

from monitor import MonitorConsumer
from database import Database, MONITOR_SCHEMA, DB
from datetime import datetime



class AlertTest(unittest.TestCase):
    ''' Test Monitor Alert system (in MonitorConsumer._collector)
        MonitorConsumer._collector returns:
        0: ok (no alert, data send to GUI)
        1: alert (send alert message to GUI)
        2: recover (send recover message to GUI)
    '''

    def setUp(self):
        ''' Initialize test variables
        '''
        self.website = 'https://test_website.test'
        self.mon = MonitorConsumer([])

    def test_alert(self):
        metrics = [0] # 0% availability
        # Assert alert send: return 1
        assert self.mon._update_system(metrics=metrics, type='watcher', website=self.website) == 1

    def test_recover(self):
        metrics = [0]
        self.mon._update_system(metrics=metrics, type='watcher', website=self.website)
        metrics = [90]
        # Assert recover send: Availability=90 > 80, return 2
        assert self.mon._update_system(metrics=metrics, type='watcher', website=self.website) == 2


# Run test in /WebMonitor => python3 test/test_monitor.py
unittest.main()
