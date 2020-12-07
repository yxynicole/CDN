mkdir -p log

if pgrep -f dnsserver &> /dev/null ; then 
    echo "dns started already"
else
    nohup ./dnsserver -p 8080 -n www.google.com &> log/dns.log &
    sleep 3
    pgrep -f dnsserver &> /dev/null && echo "dns started" || echo "dns failed to start"
fi