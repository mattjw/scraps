#!/bin/bash

# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2014
# License:  MIT License

# A wrapper around mongodump. Copies an entire mongodb instance to a directory.
# For basic backup purposes.

log=std-`date --iso-8601`.txt
dest=dump-`date --iso-8601`
echo "logging to $log"
echo "dumping to dir $dest"
echo "enter username"
read user
echo "enter password for user '$user'"
read -s passw

stdbuf -eL -oL mongodump -u $user  -p $passw --authenticationDatabase admin -o $dest > $log 2>&1  &

echo "running in background with pid $!"