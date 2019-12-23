import sqlite3
from database import DB
from datetime import datetime, timedelta
from monitor_utils import get_websites

websites = get_websites('conf.txt')

interval = 120
metrics = {'availability_rate': None,
           'avg_resp_time': None,
           'max_resp_time': None,
           'max_status_code': None,
           'avg_size': None,
           'max_size': None,
           'content-type': None}


conn = sqlite3.connect(DB)
cursor = conn.cursor()

t = (datetime.now()-timedelta(minutes=interval))
t = t.strftime('%Y-%m-%d %H:%M:%S')

for website in websites:
    # Rate of availability
    cursor.execute('''
        SELECT AVG(available) FROM Monitor WHERE date >= (?) AND website = (?)
    ''', (t,website))

    roa = cursor.fetchall()
    print(website, roa)

    # Avg response_time
    cursor.execute('''
        SELECT AVG(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
    ''', (t,website))

    art = cursor.fetchall()
    print(website, art)

    # Max response_time
    cursor.execute('''
        SELECT MAX(response_time) FROM Monitor WHERE date >= (?) AND website = (?)
    ''', (t,website))

    mrt = cursor.fetchall()
    print(website, mrt)

    # Avg size
    cursor.execute('''
        SELECT AVG(size) FROM Monitor WHERE date >= (?) AND website = (?)
    ''', (t,website))

    asize = cursor.fetchall()
    print(website, asize)

    # Max size
    cursor.execute('''
        SELECT MAX(size) FROM Monitor WHERE date >= (?) AND website = (?)
    ''', (t,website))

    msize = cursor.fetchall()
    print(website, msize)

    # Most occuring status_code
    cursor.execute('''
        SELECT status_code, COUNT(status_code) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
        GROUP BY status_code
        ORDER BY occ DESC
        LIMIT 1
    ''', (t,website))

    mcontent = cursor.fetchall()
    print(website, mcontent)


    # Most occuring content type
    cursor.execute('''
        SELECT content, COUNT(content) AS occ FROM Monitor WHERE date >= (?) AND website = (?)
        GROUP BY content
        ORDER BY occ DESC
        LIMIT 1
    ''', (t,website))

    mcontent = cursor.fetchall()
    print(website, mcontent)
