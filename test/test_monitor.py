import unittest
import sys
import os
sys.path.append('./src/')

from monitor import MonitorConsumer
from database import Database, MONITOR_SCHEMA, DB
from datetime import datetime

DB = 'test_monitor_SQLite.db'

class AlertTest(unittest.TestCase):
    ''' Test Monitor Alert system (in MonitorConsumer._collector)
        MonitorConsumer._collector returns:
        0: ok (no alert, data send to GUI)
        1: alert (send alert message to GUI)
        2: recover (send recover message to GUI)
    '''

    def _rm_db(db_file):
        if os.path.isfile(DB):
            os.remove(DB)

    def setUp(self):
        ''' Initialize test variables
        '''
        self._rm_db()
        self.record = {key:None for key in MONITOR_SCHEMA}
        self.record[MONITOR_SCHEMA[0]] = 'https://facebook.com'
        self.record[MONITOR_SCHEMA[1]] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.db = Database()
        self.mon = MonitorConsumer([])
        print(self._testMethodName)


    def test_alert(self):
        self.record[MONITOR_SCHEMA[2]] = False # not available => alert
        website = self.record[MONITOR_SCHEMA[0]]
        self.db.insert_monitor_record(self.record)

        # Assert alert send: return 1
        assert self.mon._collector(interval=10, website=website, type='watcher') == 1
        self._rm_db()


    def test_recover(self):
        self.record[MONITOR_SCHEMA[2]] = False # not available => alert
        website = self.record[MONITOR_SCHEMA[0]]
        self.db.insert_monitor_record(self.record)

        self.mon._collector(interval=10, website=website, type='watcher')

        self.record[MONITOR_SCHEMA[2]] = True # available => recover

        for _ in range(10):
            self.db.insert_monitor_record(self.record)

        # Assert recover send: Availability=90 > 80, return 2
        assert self.mon._collector(interval=10, website=website, type='watcher') == 2
        self._rm_db()

unittest.main()
