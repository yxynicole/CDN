## Project 5: Roll Your Own CDN

### Project Description

https://david.choffnes.com/classes/cs4700fa20/project5.php

You must implement a CDN using the following features. First, you will use DNS redirection to send clients to the replica server with the fastest response time. Second, you will write a simple Web server that returns content requested by clients. Third, you will implement a system that uses information about network performance, load on servers, and cached data at servers to determine the best replica server. Performance will be measured in terms of how long it takes to download a piece of content. Similar to most Web sites, most content will be small in terms of bytes.

### Design Decisions / High Level Approach
DNS Server:  We implemented a DNS server that responds with the IP address of the closest replica server based on IP Geolocation.  We used a UDPServer to listen for incoming requests and to respond with an A record.  We did not elect to use any packages to parse the DNS request and to form the response, instead we wrote this parsing and packet forming code ourselves.

HTTP Server:  We use an HTTPServer that we initiate on the replica server.  The server listens for incoming GET requests. If the requested content is cached on the server, we get the content and respond.  If the requested content is not on the replica server, we fetch the content from the origin server and response.  For cache, we have created a custom class that will hold our cache in RAM.  

Cache:  We place the popular_sites.csv file on the replica servers.  When the httpserver code is initiated, we pre-fetch as much popluar content as possible into cache.  We make get requests to the origin server for this content. Cache entries are held in memory and our replacement strategy is LRU.

### Performance Optimization

DNS Response: We direct clients to the closest replica server based on the client's location.  For each client DNS request, we determine the client's latitude and longitude based on a free IP Geolocation Service (https://ip-api.com/docs/api:json) and calculate which replica server is the closest to the client.  Although not necessarily guaranteed, the idea is that clients will have the best performance fetching client when they are fetching from the closest replica server.  We keep a list of client IP addresses that we have seen before and the corresponding closest replica server.  For IP addresses that we have seen before, we can respond immediately with the pre-determined best replica server

Cache Startegy / Optimization: 
We developed a prefetch process to cache the top pages in the popularities.csv. The pre-fetch process is executed in a background thread to reduce the service startup time, so http service can immediately serve the traffic while cache is being added in the background. We maintain a `size` variable to track how many bytes of cache in total is in the memory, and we evaluate every entry we added/removed by `sys.getsizeof` and reflect it on `size` accordingly. The cache replace strategy is Least Recently Used (LRU). Each cache entry will have a timestamp to track the most recent timestamp when it is used. That means 
1. if we find existing entry in cache, the timestamp will be refreshed;
2. if we want to add a new entry into cache and it will make total size exceed the 10 MB limit, cache manager will keep popping the lesat recently used entry by comparing the timestamp among all the existing, util cache has enough room for new entry. 

### Evaluating Performance Optimization Effectiveness
For DNS responses, we were able to manually verify that were mapping clients to the closest replica server.  For the beacon coming from Paris, we made sure our system mapped this to the Ireland Server.  For the Beacon coming from the Boston area, we made sure this was mapped to the N. Virginia server, etc.

Using time wget, we evaluated effectiveness of IP Geolocation vs. randomly picking a replica server.  On average, the wget download for the same content in cache was faster for mapped to the closer server compared to random server selection (although this was informal sampling, see future improvements section for ideas around statistical tests)

### Future Improvements (what we would do if we had more time)

1) We would implement active measurement techniques to map clients to the best replica server. For all IP addresses we have seen before, we could ping the replica servers to see which responded the fasted.  We could continually run these pings and we would be able to map clients (that we have seen before) to the replica server likely to respond the fastest. 

2) We would improve our ability to evaluate the effectiveness of our solution through automated simulation testing.  Through the automation, we could configure different versions of the CDN (IP Geolocation vs active measurement), and we could do statistical analysis on the performance metrics to assess our solution.

3) We would improve our searching algorithm to find LRU entry. The current version is doing linear search but we could improve it by applying a better algorithm.

4) We would compresss our cache entries to reduce the space it takes. This will increase total number of pages our replica servers can hold at the same time and reduce number of requests made from replica to original server.

### Code Breakdown

DNS Folder: We decided to both do separate versions of the DNS Server to start the project.  We both produced working DNS Servers that send back well-formed DNS responses.  We are using Xinyu's version of the DNS server in our submission.  

IP Geolocation methods: (Jeff)

HTTP Folder:  Server.py, Remote.py, and Cache.py files (Xinyu).  Initial read_popularity_file method (Jeff) with tweaks from (Xinyu)

Deployment Scripts: (Xinyu)


