import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from database import Database, MONITOR_SCHEMA


def get_websites(path):
    websites = []
    with open(path) as outfile:
        for website in outfile:
            websites.append(website.rstrip('\n'))
    return websites


def _monitor_website(website):
    data = dict(MONITOR_SCHEMA)
    data['website'] = website
    try:
        r = requests.get(website)
    except ConnectionError:
        data['available'] = False
        data['date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
    else:
        data['available'] = True
        data['status_code'] = r.status_code
        data['reponse_time'] = r.elapsed.total_seconds()
        data['content'] = r.headers['Content-type']
        data['date'] = r.headers['Date']
        data['size'] = len(r.content)
    finally:
        return data


def _monitor_dump(data):
    db = Database()
    db.insert_monitor_record(data)


# def main():
#     data = _monitor_website('https://github.com/9OP')
#     _monitor_dump(data)
#
# if __name__=='__main__':
#     main()
