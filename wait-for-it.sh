#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available
# See: https://github.com/vishnubob/wait-for-it

set -e

TIMEOUT=15
QUIET=0
HOST=
PORT=

usage()
{
    echo "Usage: $0 host:port [-s] [-t timeout] [-- command args]"
    exit 1
}

wait_for()
{
    for i in `seq $TIMEOUT` ; do
        nc -z "$HOST" "$PORT" > /dev/null 2>&1
        result=$?
        if [ $result -eq 0 ] ; then
            if [ $QUIET -ne 1 ] ; then
                echo "Host $HOST and port $PORT are available"
            fi
            return 0
        fi
        sleep 1
    done
    echo "Timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
    exit 1
}

while [[ $# -gt 0 ]] ; do
    case "$1" in
        *:* )
        HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
        PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [ "$TIMEOUT" = "" ] ; then
            break
        fi
        shift 2
        ;;
        --)
        shift
        break
        ;;
        --help)
        usage
        ;;
        *)
        echo "Unknown argument: $1"
        usage
        ;;
    esac
done

if [ "$HOST" = "" ] || [ "$PORT" = "" ] ; then
    echo "Error: you need to provide a host and port to test."
    usage
fi

wait_for

exec "$@"