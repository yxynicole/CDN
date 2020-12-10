## How to start server

```
python3 cs5700http/server.py -p 8081 -o ec2-18-207-254-152.compute-1.amazonaws.com:8080
```

## How to test

```
curl localhost:8081
```

## handle terminate signal
In order to gracefully handle the server termiation, we use signal library to handle terminate.

By raising sys exit, service can be shut down properly.

## Cache Strategy

We are adopting Least Receint Used (LRU). 

For each URL we are requested to original server, we maintain an entry object which holds the response content and the timestamp the URL being requested.

If the URL requested can be found in cache, we read the cache in memory, update the latest timestamp, and return the value back to client.

if the URL requested can not be found in cache, we request it from original server, save it in cache with the timestamp, and return it back to client.

The cache size is limited to be 10Mb. In order to meet the requirement, we track the total size of the cache in memory and follow the bloew algorithm. 
1. Every time the new content is added into cache, we measure the memory size of url, content, timestamp and entry object by using `sys.getsizeof`, then add it to cache size. 
2. After new content is added, cache size will be examinated: if size is above 10MB limit, then we will keep remove the entry with least recent timestamp.
3. If a cache entry was found and resent to client, the timestamp of entry will be refreshed.
4. if entry is removed as a least used entry, the cache size will be deducted accordingly.

## Prefetch the cache after server starts
In order to taking advantage of popularity.csv, we spawned a separate thread to prefetch the pages in the list from top to bottom util cache reaches limit.Using the thread is to reduce the server start up time. 

A lock is used in cache set method to avoid race condition problem.
