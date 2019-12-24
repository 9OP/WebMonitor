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
    data['website'] = website
    data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        r = requests.get(website)
    except ConnectionError:
        data['available'] = False
    else:
        data['available'] = True
        data['status_code'] = r.status_code
        data['response_time'] = r.elapsed.total_seconds()
        data['content'] = r.headers['Content-type']
        data['size'] = len(r.content)
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
    metrics = db.get_monitor_metrics(t, website)
    metrics = [metrics[key] for key in MONITOR_METRICS]
    return metrics


def _metrics_print(website, interval, metrics):
    print('{:<10}{:<5}{:<10}{}'.format('Interval:', str(interval/60)+'min', 'Website:', website))
    print('-'*50)
    for metric, val in metrics.items():
        print('{:<35}{}'.format(metric+': ', val))
    print('-'*50)
    print('\n')
