import psutil

class CacheEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 0

    def incr(self):
        self.freq += 1


class Cache:
    def __init__(self):
        self.entries = {}

    def has(self, key):
        return key in self.entries

    def get(self, key):
        entry = self.entries[key]
        entry.incr()
        return entry.value

    def set(self, key, value):
        entry = CacheEntry(key, value)
        while self.out_of_room(entry):
            self.remove_least_useful_entry()
        self.entries[key] = entry

    def out_of_room(self, entry):
        # TODO
        return psutil.Process().memory_info().rss / 1024 ** 2 > 100

    def remove_least_useful_entry(self):
        key, freq = None, None
        for entry in self.entries:
            if freq is None or freq > entry.freq:
                key = entry.key

        if key:
            del self.entries[key]
