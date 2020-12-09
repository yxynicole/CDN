# import psutil

import csv, os
from cs5700http import remote

POPULATIRY_FILE = "popular_sites.csv"
ORIGIN_SERVER = 'ec2-18-207-254-152.compute-1.amazonaws.com:8080'

class Cache:
    def __init__(self):
        self.popular_sites = [] # List to store popular sites, [path:# of views]
        self.entries = {}
        self.read_popularity_file()
        self.populate_cache(ORIGIN_SERVER)

    def read_popularity_file(self):
        '''
        Reads from the popular_sites.csv and poulates the popular_sites array
        Each array element containts [path, num visits]
        '''
        if not os.path.exists(POPULATIRY_FILE):
            return

        with open(POPULATIRY_FILE, 'r') as file:
            reader = csv.reader(file)
            reader_iterable = iter(reader)
            next(reader_iterable)
            for row in reader_iterable:
                self.popular_sites.append([row[0][24:], int(row[1])]) #Gets starting at /wiki
    
    def populate_cache(self, origin_server):
        for site in self.popular_sites[:10]:
            status_code, content, error = remote.get(ORIGIN_SERVER, site[0])
            if error is None:
                self.entries[site[0]] = content
            else:
                print("not running")
        # print(self.entries['/wiki/Patrick_Mahomes'])


    def has(self, key):
        return key in self.entries.keys()

    def get(self, key):
        return self.entries.get(key)

    # def set(self, key, value):
    #     entry = CacheEntry(key, value)
    #     # while self.out_of_room(entry):
    #     #     self.remove_least_useful_entry()
    #     self.entries[key] = entry

    # def out_of_room(self, entry):
    #     # TODO
    #     return psutil.Process().memory_info().rss / 1024 ** 2 > 100

    # def remove_least_useful_entry(self):
    #     key, freq = None, None
    #     for entry in self.entries:
    #         if freq is None or freq > entry.freq:
    #             key = entry.key

    #     if key:
    #         del self.entries[key]
