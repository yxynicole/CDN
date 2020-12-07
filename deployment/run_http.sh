mkdir -p log

if pgrep -f httpserver &> /dev/null ; then 
    echo "http started already"
else
    nohup ./httpserver -p 8080 -o www.google.com &> log/http.log &
    sleep 3
    pgrep -f httpserver &> /dev/null && echo "http started" || echo "http failed to start"
fi