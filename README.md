# WebMonitor

This is a python application that monitors websites and compute relevant
metrics such as availability rate, response time, status code occurence etc...

The project is developped in python and gtk.

websites.txt contains the sites to monitor, the format is:
```
https://example1.com, check_interval1(in seconds)
https://example2.com, check_interval2
https://example3.com, check_interval3
```

WebMonitor relies on Schedulers and thread and is based on a Producer-Consumer
design pattern.


**To do:**
- [X] Schedulers and MonitorMaster
- [X] Backend
- [X] UI
- [X] Watchers for alert and recover
- [X] Tests for watcher recover and alert system

### Installation

**Steps:**
- 1) download the repo, ``` $ git clone https://github.com/9OP/WebMonitor```
- 2) install the dependancies, ``` $ pip3 install -r requirements.txt```
- 3) execute DDmonitor ``` $ sh ./DDmonitor ```

### Improvement
Overall I think the **design is pretty strong.**:
- **MVC architecture**, the GUI, MonitorMaster, and DB are cleanly separated.
- **Schedulers**, launch threads with a certain frequence
- **SQLite DB and Database class interface**, enable persistence of monitoring

Some improvement on the GUI are possible, designing an UI is a very difficult taks and comming up with something easy to use pretty is not trivial.

Also some parameters are hardcoded and not availble to the user (for instance look back perdiod and update intervals for the Schedulers).

**Concerns and Warnings:**

SQLite dabatase doesnt not handle well multi connection writting, this is possible that while running the database stop connection and lock itsel. One improvement would be to use MUTEX (threading Lock) to make sure no Schedulers are writting at the same time. This is clearly is small change on the code (pass a lock variable to Schedulers, lock and unlock db when writting). I did not do it for several reasons:
- keep code simple (ideas are more important),
- this is a small projects no need to try hard,
- If we move to another db engine, the lock will be useless, this is mostly a SQLite limitations (every proper db engine supports concurrent access in R/W).
