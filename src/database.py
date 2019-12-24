import sqlite3
import os.path
from sqlite3 import Error


DB = 'monitor_SQLite.db'
MONITOR_SCHEMA = ['website',
                  'date',
                  'available',
                  'response_time',
                  'status_code',
                  'size',
                  'content']
MONITOR_METRICS = ['Availability',
                   'Website',
                   'Avg resp time',
                   'Max resp time',
                   'Status code',
                   'Avg size',
                   'Max size',
                   'Content']
TABLES = {
'Monitor': '''
CREATE TABLE Monitor (
    website TEXT,
    date DATE,
    available BOOLEAN,
    response_time TIME,
    status_code INTEGER,
    size INTEGER,
    content TEXT
);
'''
}


class Database:
    ''' Interface class with project sqlite database.
        Ensure consistent access to the database.
    '''

    def __init__(self, db_file=DB):
        self.db_file = db_file
        self._connection = self._create_connection()
        self._cursor = self._connection.cursor()

    def __del__(self):
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

    def _create_connection(self):
        ''' create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        '''
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def _create_table(self, table):
        ''' create TABLES[table] in database
        :param table: key in TABLES global variable - table name
        '''
        try:
            self._cursor.execute(TABLES[table])
            self._connection.commit()
        except Error as e:
            print(e)

    def insert_monitor_record(self, record):
        ''' insert record in monitor table
        :param monitor: record to insert in Monitor table
        '''
        self._cursor.execute('''
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Monitor'
        ''')
        if self._cursor.fetchone()[0]!=1: # create table if doesn't exist
            self._create_table('Monitor')

        self._cursor.execute('''
            INSERT INTO Monitor VALUES (?,?,?,?,?,?,?)
        ''', tuple([record[key] for key in MONITOR_SCHEMA]))
        self._connection.commit()

    def get_monitor_metrics(self, date, website):
        ''' Collect compute and return metrics for the
            look back until now interval
        :param date: date from which start to compute metrics
        :return metrics dict

        ex: date format: YYYY-MM-DD HH:MM:SS
        '''
        metrics = {}

        # Return str(x)
        formater0 = lambda x: str(x) if (x is not None) else None

        # Return rounded time x
        formater1 = lambda x: str(round(x, 4))+' s' if (x is not None) else None

        # Return rounded kb size x
        formater2 = lambda x: str(round(x/1000, 2))+' Kb' if (x is not None) else None


        # Rate of availability
        self._cursor.execute('''
            SELECT AVG(available) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics[MONITOR_METRICS[0]] = int(self._cursor.fetchall()[0][0])*100

        # Website
        metrics[MONITOR_METRICS[1]] = website

        # Avg response_time
        self._cursor.execute('''
            SELECT AVG(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        # metrics[MONITOR_METRICS[2]] = str(round(self._cursor.fetchall()[0][0])
        metrics[MONITOR_METRICS[2]] = formater1(self._cursor.fetchall()[0][0])

        # Max response_time
        self._cursor.execute('''
            SELECT MAX(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics[MONITOR_METRICS[3]] = formater1(self._cursor.fetchall()[0][0])

        # Most occuring status_code
        self._cursor.execute('''
            SELECT status_code, COUNT(status_code) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
            GROUP BY status_code
            ORDER BY occ DESC
            LIMIT 1
        ''', (date, website))
        metrics[MONITOR_METRICS[4]] = formater0(self._cursor.fetchall()[0][0])

        # Avg size
        self._cursor.execute('''
            SELECT AVG(size) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics[MONITOR_METRICS[5]] = formater2(self._cursor.fetchall()[0][0])

        # Max size
        self._cursor.execute('''
            SELECT MAX(size) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics[MONITOR_METRICS[6]] = formater2(self._cursor.fetchall()[0][0])

        # Most occuring content type
        self._cursor.execute('''
            SELECT content, COUNT(content) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
            GROUP BY content
            ORDER BY occ DESC
            LIMIT 1
        ''', (date, website))
        metrics[MONITOR_METRICS[7]] = formater0(self._cursor.fetchall()[0][0])

        return metrics
