#!/bin/bash
# Arguments:
# 1: Number of times python script should be run
# 2: Input file
# 3: Output file
# 4: Number of nodes
# 5: Timeout

NUMTIMES=$1

for i in $(seq 1 $NUMTIMES); do
    exec python main.py $2 $3 1 info >logs/temp.log &
    PID=$!
    sleep $5
    if ps -p $PID >/dev/null; then
        echo "$PID is running"
        # kill the process
        kill -SIGINT $PID
        cp logs/temp.log logs/inp-$4-info.log
        break
    fi
    echo "Completed run "$i
done
