# Deployment instructions

## 1. add execute permission to deployment scripts, this can be done by `make` command
```bash
$ make
chmod +x httpserver dnsserver
chmod +x deployCDN runCDN stopCDN
```
NOTE - make file adding execute permission for all the executable scripts, but only deploy|run|stopCDN required for deploying from your local machine

## 2. deploy to DNS & replica servers
```bash
$ ./deployCDN -u xinyuye -i ~/.ssh/id_ed25519 -o ec2-18-207-254-152.compute-1.amazonaws.com -p 50000 -n cs5700cdn.example.com
deploying to cs5700cdnproject.ccs.neu.edu
......................
... output omitted ...
......................
deployment to ec2-18-231-122-62.sa-east-1.compute.amazonaws.com is done
All deployments are done
```

This will execute the deployment script, which will ssh to dns server (cs5700cdnproject.ccs.neu.edu) and all the replica servers listed in `deployment/replicas.txt`(copyed from `/course/cs5700f20/ec2-hosts.txt`)
 and create directory `~/CDN` then scp the source code and run the makefile
 
 
## 3. start services
```bash
$ ./runCDN -u xinyuye -i ~/.ssh/id_ed25519 -o ec2-18-207-254-152.compute-1.amazonaws.com -p 50000 -n cs5700cdn.example.com
start dns service on cs5700cdnproject.ccs.neu.edu
dns started
====
start http service on ec2-34-238-192-84.compute-1.amazonaws.com
http started
----
start http service on ec2-13-231-206-182.ap-northeast-1.compute.amazonaws.com
http started
----
start http service on ec2-13-239-22-118.ap-southeast-2.compute.amazonaws.com
http started
----
start http service on ec2-34-248-209-79.eu-west-1.compute.amazonaws.com
http started
----
start http service on ec2-18-231-122-62.sa-east-1.compute.amazonaws.com
http started
----
```

The command will start the dns server on cs5700cdnproject.ccs.neu.edu, and http server on replicas.

### How it runs
per requirement, there are two files `dnsserver` and `httpserver` served as main entry point of dns and http service. However, these two command running server synchronously. In order to execute them asynchronously, we created a few bash script under the `deployment/` directory:

>run_http.sh  
>run_dns.sh  
>stop_http.sh  
>stop_dns.sh  


`run_http.sh` & `run_dns.sh` will use `nohup` and `&` to execute the `httpserver` & `dnsserver` in the background.

`stop_http.sh` & `stop_dns.sh` will search process by name and uid and kill them

## 4 Test and troubleshooting
we can `dig` dns service, `wget`|`curl` http service or open the url in browswer to check if it works

#### troubleshoot
dns and http service will save log under `~/log/` on the server, and name of the log will be dns|http_<server_start_time>.log.


for example - to check the log of running http service
```bash
tail -f ~/log/http*
```

## 5. stop the services

```bash
$ ./stopCDN -u xinyuye -i ~/.ssh/id_ed25519
stop dns service on cs5700cdnproject.ccs.neu.edu
dns stopped
====
stop http service on ec2-34-238-192-84.compute-1.amazonaws.com
http stopped
----
stop http service on ec2-13-231-206-182.ap-northeast-1.compute.amazonaws.com
http stopped
----
stop http service on ec2-13-239-22-118.ap-southeast-2.compute.amazonaws.com
http stopped
----
stop http service on ec2-34-248-209-79.eu-west-1.compute.amazonaws.com
http stopped
----
stop http service on ec2-18-231-122-62.sa-east-1.compute.amazonaws.com
http stopped
----
```

