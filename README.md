# WebMonitor

Python websites monitoring desktop application.
Compute relevant metrics such as availability rate, response time, status code occurence etc...

websites.txt contains the sites to monitor, the format is:
```
https://example1.com, check_interval1(in seconds)
https://example2.com, check_interval2
https://example3.com, check_interval3
```

### Installation

- Download repo, ``` $ git clone https://github.com/9OP/WebMonitor```
- Create venv, ``` $python3 -m venv WebMonitor/venv/ ```
- Activate venv, ``` $source WebMonitor/venv/bin/activate ```
- Install lib gi, ``` sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 ```
- Install dependancies, ``` $pip3 install -r requirements.txt ```



**To do:**
- [X] Schedulers and MonitorMaster
- [X] Backend
- [X] UI
- [X] Watchers for alert and recover
- [X] Tests for watcher recover and alert system
- [X] Installation procedure (Windows and linux)
- [X] Threads Mutex (avoid segfault when sending alert to GUI)
