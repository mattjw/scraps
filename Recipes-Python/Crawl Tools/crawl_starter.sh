#!/bin/bash

nohup stdbuf -eL -oL \
    python crawl_starter_demo.py \
    > ./log/stdboth.out 2>&1 \
    &

pid=$!
echo $pid > ./log/process.pid
echo "pid $pid"