import requests
from requests.exceptions import ConnectionError
from datetime import datetime, timedelta
from database import Database, MONITOR_SCHEMA, MONITOR_METRICS


def get_websites(path):
    ''' Return websites from file path.
    :param path: path to a file containing website addresses
    :return list of websites
    '''
    websites = []
    delays = []
    with open(path) as outfile:
        for line in outfile:
            website = line.split(', ')[0].rstrip('\n')
            delay = line.split(', ')[1].rstrip('\n')
            websites.append(website)
            delays.append(int(delay))

    return delays, websites


def _monitor_website(website):
    ''' Monitor website: return raw monitoring data from website
    :param website: http addresse of website to monitor
    :return monitored website data
    '''
    data = {key: None for key in MONITOR_SCHEMA}
    data[MONITOR_SCHEMA[0]] = website # website
    data[MONITOR_SCHEMA[1]] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # date
    try:
        r = requests.get(website)
    except ConnectionError:
        data[MONITOR_SCHEMA[2]] = False
    else:
        data[MONITOR_SCHEMA[2]] = True # available
        data[MONITOR_SCHEMA[3]] = r.elapsed.total_seconds() # response_time
        data[MONITOR_SCHEMA[4]] = r.status_code # status_code
        data[MONITOR_SCHEMA[5]] = len(r.content) # size
        data[MONITOR_SCHEMA[6]] = r.headers['Content-type'] # content

    finally:
        return data


def _monitor_dump(data):
    ''' Dump monitor data into project database monitor table
    :param data: database monitor table record (following MONITOR_SCHEMA)
    '''
    db = Database()
    db.insert_monitor_record(data)


def _monitor_collect(interval, website):
    ''' Collect and compute metrics between now-interval(seconds) and now
    :param interval: look back interval to compute/collect metrics
    '''
    t = datetime.now()-timedelta(minutes=interval)
    t = t.strftime('%Y-%m-%d %H:%M:%S')
    db = Database()
    metrics = {key: None for key in MONITOR_METRICS}
    try:
        metrics = db.get_monitor_metrics(t, website)
    finally:
        metrics = [metrics[key] for key in MONITOR_METRICS]
        return metrics
