while getopts p:o: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
        o) origin=${OPTARG};;
    esac
done

mkdir -p ~/log

if pgrep -u $UID -f httpserver &> /dev/null ; then 
    echo "http started already"
    pgrep -u $UID -f httpserver | xargs ps -up
else
    logname=$(date +%F-%H-%M-%S)
    nohup ./httpserver -p $port -o $origin &> ~/log/http_$logname.log &
    sleep 3
    pgrep -u $UID -f httpserver &> /dev/null && echo "http started" || echo "http failed to start"
fi