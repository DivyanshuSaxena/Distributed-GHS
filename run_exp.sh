#!/bin/bash
# Arguments:
# 1: Number of times python script should be run
# 2: Input file
# 3: Number of nodes
# 4: Timeout

NUMTIMES=$1

for i in $(seq 1 $NUMTIMES); do
    exec python main.py 1 basic $2 >logs/temp.log &
    PID=$!
    sleep $4
    if ps -p $PID >/dev/null; then
        echo "$PID is running"
        # kill the process
        kill -SIGINT $PID
        cp logs/temp.log logs/inp-$3-basic.log
        break
    fi
    tail -5 logs/temp.log
    truncate -s 0 logs/temp.log
    kill -9 $PID
    echo "Completed run "$i
done
