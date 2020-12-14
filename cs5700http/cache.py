# import psutil

import sys, csv, os, time, threading, functools
from cs5700http import remote

print = functools.partial(print, flush=True)

POPULATIRY_FILE = "popular_sites.csv"
MAX_CACHE_SIZE = 10 * 1024 ** 2  # 10MB

class CacheEntry:
    #__slots__ = ('v', 't')
    def __init__(self, value, t):
        self.v = value
        self.t = t

    def refresh(self):
        self.t = time.time()


class Cache:
    def __init__(self):
        self.lock = threading.Lock()
        self.entries = {}
        self.size = 0

    def read_popularity_file_and_pupulate_cache(self):
        '''
        Reads from the popular_sites.csv and poulates the popular_sites array
        Each array element containts [path, num visits]
        '''
        if not os.path.exists(POPULATIRY_FILE):
            return
        print('Reading popularity file and caching the pages')
        with open(POPULATIRY_FILE, 'r') as file:
            reader = csv.reader(file)
            reader_iterable = iter(reader)
            next(reader_iterable)
            init_time = time.time()
            for row in reader_iterable:
                path = row[0][24:] #Gets starting at /wiki
                print('Caching path', path)
                status_code, content, error = remote.get(path)
                if error is None:
                    cache_full = self.set(path, content, init_time)
                    init_time -= 1
                    if cache_full:
                        return

    def has(self, key):
        return key in self.entries

    def get(self, key):
        entry = self.entries[key]
        entry.refresh()
        return entry.v

    def set(self, key, value, t=None):
        if t is None:
            t = time.time()
        with self.lock:
            entry = CacheEntry(value, t)
            self.entries[key] = entry
            self.size += sys.getsizeof(entry) + sys.getsizeof(key) + sys.getsizeof(entry.t) + sys.getsizeof(entry.v)
            if self.out_of_room():
                enough_room = False
                while not enough_room:
                    self.remove_least_recent_used_entry()
                    enough_room = not self.out_of_room()
                return True
            else:
                return False

    def out_of_room(self):
        print('checking size', self.size)
        if self.size > MAX_CACHE_SIZE:
            print('Out of room!')
            return True
        else:
            return False

    def remove_least_recent_used_entry(self):
        least_used, t = None, None
        for path, entry in self.entries.items():
            if t is None or t > entry.t:
                least_used = path
                t = entry.t
        if least_used:
            entry = self.entries[least_used]
            self.size -= sys.getsizeof(entry) + sys.getsizeof(least_used) + sys.getsizeof(entry.t) + sys.getsizeof(entry.v)
            del self.entries[least_used], entry
            print('removed least recent used cache for path', least_used)
