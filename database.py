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
