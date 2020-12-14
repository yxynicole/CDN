## Project 5: Roll Your Own CDN

This project is due at 11:59pm on December 14, 2020. The milestone is due at 11:59pm on December 7, 2020. 
https://david.choffnes.com/classes/cs4700fa20/project5.php

### Project Requirements
You must implement a CDN using the following features. First, you will use DNS redirection to send clients to the replica server with the fastest response time. Second, you will write a simple Web server that returns content requested by clients. Third, you will implement a system that uses information about network performance, load on servers, and cached data at servers to determine the best replica server. Performance will be measured in terms of how long it takes to download a piece of content. Similar to most Web sites, most content will be small in terms of bytes.

### What we implemented
1) DNS Server.  Responds to dig requests with the IP address of the closest replica server (based on IP Geolocation)
2) HTTP Server. Deployed to the EC2 replica servers.  Pre-fetches content for cache (via GETs to Origin sever) from the provided popular_sites.csv file. Implements a cache replacement strategy.  Efficiently fetches content from the origin when content is not in cache
3) Deploy, Run, and Stop CDN scripts to manage our CDN

### Final report
Please see the Final Report file for more information


