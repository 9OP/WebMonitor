# WebMonitor

Python websites monitoring desktop application.
Compute relevant metrics such as availability rate, response time, status code occurence etc...

websites.txt contains the sites to monitor, the format is:
```
https://example1.com, check_interval1(in seconds)
https://example2.com, check_interval2
https://example3.com, check_interval3
```

![Image of WebMonitor](https://github.com/9OP/WebMonitor/blob/master/resources/media/webmonitor.png)

### Installation

[LINUX]
- Download repo, ``` $ git clone https://github.com/9OP/WebMonitor ```
- Run install script, ``` $ sh install.sh ```
- Launch, ``` $ webmonitor ```, the launch icon should be available in the explorer


**To do:**
- [X] Schedulers and MonitorMaster
- [X] Backend
- [X] UI
- [X] Watchers for alert and recover
- [X] Tests for watcher recover and alert system
- [X] Installation procedure (Linux)
- [X] Threads Mutex (avoid segfault when sending alert to GUI)
- [ ] Create pypi package (setup.py) for cross plaform Windows and OSX installation
