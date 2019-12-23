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
# MONITOR_METRICS =
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
        :return metrics

        ex: date format: YYYY-MM-DD HH:MM:SS
        '''
        # self._cursor.execute('''
        #     SELECT date FROM Monitor WHERE date >= (?) AND website = (?)
        # ''', (date, website))

        metrics = {}

        # Rate of availability
        self._cursor.execute('''
            SELECT AVG(available) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics['availability_rate'] = self._cursor.fetchall()[0]

        # Avg response_time
        self._cursor.execute('''
            SELECT AVG(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics['avg_response_time'] = self._cursor.fetchall()[0]

        # Max response_time
        self._cursor.execute('''
            SELECT MAX(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics['max_response_time'] = self._cursor.fetchall()[0]

        # Avg size
        self._cursor.execute('''
            SELECT AVG(size) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics['average_size'] = self._cursor.fetchall()[0]

        # Max size
        self._cursor.execute('''
            SELECT MAX(size) FROM Monitor WHERE date >= (?) AND website = (?)
        ''', (date, website))
        metrics['max_size'] = self._cursor.fetchall()[0]

        # Most occuring status_code
        self._cursor.execute('''
            SELECT status_code, COUNT(status_code) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
            GROUP BY status_code
            ORDER BY occ DESC
            LIMIT 1
        ''', (date, website))
        metrics['most_occuring_status_code'] = self._cursor.fetchall()[0]

        # Most occuring content type
        self._cursor.execute('''
            SELECT content, COUNT(content) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
            GROUP BY content
            ORDER BY occ DESC
            LIMIT 1
        ''', (date, website))
        metrics['most_occuring_content_type'] = self._cursor.fetchall()[0]

        return metrics
