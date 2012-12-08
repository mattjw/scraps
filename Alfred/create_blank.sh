#!/bin/bash
# 
# Create an empty plain text file at the current Finder
# location. File is named "blank.txt" or, if a query parameter
# is given, its value will be used.
#
# Destination for file chosen in following order:
#   1. if a directory is selected, then in that directory
#   2. if a file is selected, then the same directory as the file
#   3. if nothing in Finder is selected, then at the Finder window's 
#      currently open directory
#   4. if no finder window is open, then on the desktop
# If there is already a file with the same name in the 
# target directory, then nothing happens.

# Get file name from (optional) Alfred query parameter
fname="{query}"
len=${#fname}
if [ $len -eq 0 ];
then
	# String is empty, use default.
	fname="blank.txt"
fi

# Get path of current Finder window's selected item (AppleScript code; 
# via here-script).
# If no selected item, then get the directory of the Finder window
# If still nothing, then default to Desktop
path=`osascript<<END
-- first attempt: get the current finder selection
try
    tell application "Finder" 
		set selected_item to (the selection) as alias 
		set selected_item_path to POSIX path of selected_item
		return selected_item_path
    end tell
end try
-- second attempt: get the directory of the current finder window
try
    tell application "Finder" 
        set this_directory to (the target of the front window) as alias
        set this_directory to POSIX path of this_directory
        return this_directory
    end tell
end try
-- final attempt: get the desktop
set this_directory to POSIX path of (path to desktop) 
return this_directory
END`


if [ -f $path ]
then
	# So, file, we meet again.
	# Let's find your directory instead, OK?
	path=`dirname "$path"`
fi


if [ ! -d $path ]
then
	# Oh no, it's STILL not a directory?!
	# We have failed. Seppuku!
	exit 1
fi

newfile="$path/$fname"
if [ -e "$newfile" ]
then
	# Eee gad. There's already something there! And it's ALIVE.
	# Let's get out of here while we still can!
	exit 1
fi

# Let's create the file!
touch "$newfile"



