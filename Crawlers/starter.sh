#!/bin/bash

nohup stdbuf -eL -oL \
    python demo.py \
    > ./log/stdboth.out 2>&1 \
    &

pid=$!
echo $pid > ./log/process.pid
echo "pid $pid"