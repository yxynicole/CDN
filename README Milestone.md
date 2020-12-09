## Project 5: Roll Your Own CDN

### High Level Approach
DNS Server:  For milestone 1, we implemented a simple DNS server that responds with a hardcoded IP address.  We used a UDPServer to listen for incoming requests and to respond with an A record.  We did not elect to use any packages to parse the DNS request and to form the response, instead we wrote this parsing and packet forming code ourselves.

HTTP Server:  We use an HTTPServer that we initiate on the replica server.  The server listens for incoming GET requests. If the requested content is cached on the server, we get the content and respond.  If the requested content is not on the replica server, we fetch the content from the origin server and response.  For cache, we have created a custom class that will hold our cache in RAM.  

Cache:  We place the popular_sites.csv file on the replica server.  When the httpserver code is initiated, the top 10 pieces of content are read from the csv file.  We make get requests to the origin server for this content and store the path:html in a dictionary in our custom Cache class.  This is just a preliminary strategy and we will eventually expand our cache to include as much content as the memory restrctions allow.

Note:  We have manually placed the csv file on the server to allow our cache to populate.  We still need to make this part of our deployment process. 

### Performance Optimization
Since we know the popular content ahead of time, we fetch the popular content from the origin server and cache even before any client requests it.  This will allow us to immediately server the popular content from cache when the requests start coming in.  For cache, we think RAM will be faster than reading from disk so we will try to use RAM when possible.  

While not implemented as part of milestone 1 code yet, we will be doing active measurement in order to determine the best replica server to map clients to.  Based on the clients IP address, we will determine which replica server has the lowest latency to reach the client.

### Challenges
Getting our working environment setup (understanding and accessing the different servers) took a little longer than anticipated.  Also creating a well-formed DNS response took several tries to get working

### Code Breakdown

DNS Server: We decided to both do separate versions of the DNS Server to start the project.  We both produced working DNS Servers that send back well-formed DNS responses.  We are using Xinyu's version of the DNS server in our submission

HTTP Server:  Server and Remote files (Xinyu).  Cache file (Jeff)
