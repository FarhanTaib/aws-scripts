#!/bin/bash
#
# Author: Mohd Farhan Bin Taib
# Creation date: 2nd Aug 2017
# About: Wrapper script to get CloudWath log events.
#
# Compatibility: CentOS and MacOS

export PATH=$HOME/bin:/usr/local/bin:~/.local/bin:$PATH

f_init()
{
    EPNOW=""
    EPBEF=""
    TIME=""
    FILE=""
}

f_usage()
{
cat << EOF
usage: $0 options [argument]

OPTIONS:
   -t   UTC time in below format
        "%Y-%m-%d %H:%M:%S"
        Ex: "2017-08-01 01:30:00"
   -g   CloudWatch - Log Groups name
   -r   time range in seconds (T-?)
   -o   path to filename
EOF
}

f_gettime()
{
    case $(uname -s) in
        Linux)
            OSVER="linux"
            EPNOW=$(date -ud "$TIME" "+%s000")
            #EPBEF=$(date -ud "$TIME 30 minutes ago" "+%s000")
            #EPBEF=$(date -ud "$TIME $RANGE minutes ago" "+%s000")
            EPBEF=$(date -ud "$TIME $RANGE seconds ago" "+%s000")
            ;;
        Darwin)
            OSVER="macos"
            EPNOW=$(date -u -j -f "%Y-%m-%d %H:%M:%S" "$TIME" "+%s000")
            #EPBEF=$(date -u -j -f "%Y-%m-%d %H:%M:%S" "-v-30M" "$TIME" "+%s000")
            RANGE2=$(echo $RANGE"S")
            EPBEF=$(date -u -j -f "%Y-%m-%d %H:%M:%S" "-v-$RANGE2" "$TIME" "+%s000")
            ;;
        *)
            OSVER="null"
            ;;
    esac
}


f_getlog()
{
    aws logs filter-log-events --log-group-name $GRPNAME --start-time $EPBEF --end-time $EPNOW > $FILE
}

#### MAIN ####
if [ $# -eq 0 ]; then
    f_usage
    exit 1
fi

f_init

while getopts ":h:t:g:r:o:" OPTION
do
     case $OPTION in
        h)
            f_usage
            exit 0
            ;;
        t)
            TIME=$OPTARG
            #echo $TIME
            ;;
        g)
            GRPNAME=$OPTARG
            #echo $GRPNAME
            ;;
        r)
            RANGE=$OPTARG
            #echo $RANGE
            ;;
        o)  
            FILE=$OPTARG
            touch ./$FILE
            cat /dev/null > ./$FILE
            #echo $FILE
            ;;
        *)
            f_usage
            break
            ;;
     esac
done
shift $((OPTIND -1))

f_gettime
f_getlog
if [ ! -f $FILE ]; then
    echo "File not found! something goes wrong"
else
    echo "File created: $(ls -ld $FILE)"
fi
f_init
exit 0
