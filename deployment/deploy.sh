while getopts p:o:n:u:i:t: flag
do
    case "${flag}" in
        p) port=${OPTARG};;
        o) origin=${OPTARG};;
        n) name=${OPTARG};;
        u) username=${OPTARG};;
        i) keyfile=${OPTARG};;
        t) target=${OPTARG};;
    esac
done

ssh -i $keyfile $username@$target "rm -rf ~/CDN && mkdir -p ~/CDN"
scp -i $keyfile -r [!.]* $username@$target:~/CDN/
