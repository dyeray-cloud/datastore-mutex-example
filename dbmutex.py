from google.appengine.ext import ndb
import time


class SemaphoreStorage(ndb.Model):
    counter = ndb.IntegerProperty()


class Mutex:

    def __init__(self, key=None, sleep_sec=0.5):
        if key is not None:
            self.key = key
        else:
            self.key = ndb.Key(SemaphoreStorage, 'default')
        self.sleep_sec = sleep_sec
        self.create()

    def wait(self):
        while not self._get_mutex():
            time.sleep(self.sleep_sec)

    @ndb.transactional
    def create(self):
        if not self.key.get():
            SemaphoreStorage(key=self.key, counter=1).put()

    @ndb.transactional(retries=10)
    def signal(self):
        obj = self.key.get()
        obj.counter = 1
        obj.put()

    @ndb.transactional(retries=10)
    def _get_mutex(self):
        obj = self.key.get()
        counter = obj.counter
        if counter == 1:
            obj.counter = 0
        obj.put()
        return counter
