while getopts p:n: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
        n) name=${OPTARG};;
    esac
done

mkdir -p ~/log

if pgrep -u $UID -f dnsserver &> /dev/null ; then 
    echo "dns started already"
    pgrep -u $UID -f dnsserver | xargs ps -up
else
    logname=$(date +%F-%H-%M-%S)
    nohup ./dnsserver -p $port -n $name &> ~/log/dns_$logname.log &
    sleep 3
    pgrep -u $UID -f dnsserver &> /dev/null && echo "dns started" || echo "dns failed to start"
fi