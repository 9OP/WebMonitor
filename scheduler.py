from threading import Timer


class Scheduler:
    ''' Schedule task/funtion every X seconds
    :param delay: intervals in seconds between tasks launching
    :param funtion: task to execute
    :param args: function arguments
    '''
    
    def __init__(self, delay, function, *args):
        self.function = function
        self.delay = delay
        self.args = args
        self._timer = None
        self.running = False

    def _run(self):
        self.running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.running:
            self._timer = Timer(self.delay, self._run)
            self._timer.setDaemon(True)
            self._timer.start()
            self.running = True

    def stop(self):
        self._timer.cancel()
        self.running = False
