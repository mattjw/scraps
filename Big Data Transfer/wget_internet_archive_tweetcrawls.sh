#!/bin/bash

wget  --progress=dot:giga   -a archiveteam-twitter-stream-2015-05.log   -O archiveteam-twitter-stream-2015-05.zip  --continue   "https://ia801304.us.archive.org/zip_dir.php?path=/20/items/archiveteam-twitter-stream-2015-05.zip&formats=TAR,METADATA"   & 
pid=$!
echo $pid > archiveteam-twitter-stream-2015-05.pid
echo $pid

wget  --progress=dot:giga   -a archiveteam-twitter-stream-2015-04.log   -O archiveteam-twitter-stream-2015-04.zip  --continue   "https://ia800305.us.archive.org/zip_dir.php?path=/11/items/archiveteam-twitter-stream-2015-04.zip&formats=TAR,METADATA"   & 
pid=$!
echo $pid > archiveteam-twitter-stream-2015-04.pid
echo $pid


