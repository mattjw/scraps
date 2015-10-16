#!/bin/bash

echo "twofishes-start.sh -- running"

SERVER_JAR="/opt/twofishes/twofishes-server-assembly.jar"
INDEX_DIRECTORY="/export/twofishes/twofishes-index"

echo "starting..."
echo $SERVER_JAR
echo $INDEX_DIRECTORY

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

echo $LC_ALL
echo $LANG
echo $LANGUAGE

stdbuf -eL -oL    java -jar $SERVER_JAR --hfile_basepath $INDEX_DIRECTORY     >> /opt/twofishes/logs/stdboth.log 2>&1