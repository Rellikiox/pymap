#!/bin/bash

set -e


# trap ctrl-c and call kill_server()
trap kill_server INT

function kill_server() {
    pid_to_kill="$(ps -aux | grep server.py | grep -v grep | awk '{ print $2 }')"
    if [[ -n $pid_to_kill ]]; then
        kill -9 $pid_to_kill
    fi
}


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


python $DIR/server.py &

while inotifywait -qr --event modify --format '' $DIR/*.py
do
    kill_server
    python $DIR/server.py &
done
