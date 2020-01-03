# WebMonitor

Python application that monitors websites and compute relevant
metrics such as availability rate, response time, status code occurence etc...

websites.txt contains the sites to monitor, the format is:
```
https://example1.com, check_interval1(in seconds)
https://example2.com, check_interval2
https://example3.com, check_interval3
```

**To do:**
- [X] Schedulers and MonitorMaster
- [X] Backend
- [X] UI
- [X] Watchers for alert and recover
- [X] Tests for watcher recover and alert system
- [ ] Installation procedure (Windows and linux)
- [ ] Tests
- [ ] Lock on database

### Installation

**Steps:**
- 1) download the repo, ``` $ git clone https://github.com/9OP/WebMonitor```
- 2) install the dependancies, ``` $ pip3 install -r requirements.txt```
- 3) execute DDmonitor ``` $ sh ./DDmonitor ```
