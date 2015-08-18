#!/bin/bash
#
# Sync local and remote directories.
#
# Allows per-directory control of pushed files, and exclusion of files and
# directories.
# Allows per-directory pulling of particular files and directories.
#
# Warning: be careful with directory paths and forward slashes!


#
#
# SETUP
#
host=xpizza

# paths to local and remote directories that are to be mirrored
lprefix="./stinfoprop/"  # local dir fpath
rprefix="~/Research/stnets/stinfoprop/"  # remote dir fpath

#
# dirs to copy
#push=("datasets/dat_flightsFAA/" "datasets/dat_underground/")
#pull=("out_viz/" "dat_experiments/" "out_plots/")

# list of local directories to push, relative to `lprefix`
push=(".")

# files and directories to exclude from push
push_excludes="--exclude=out_plots --exclude=out_viz --exclude=_doc --exclude=*.pyc --exclude=dat_experiments --exclude=dat_results"

# list of remote directories to pull, relative to `rprefix`
pull=("out_plots/" "dat_experiments/" "dat_results/" "out_viz/")


#
#
# SYNC
#

echo
echo "pushing"
echo
for pth in "${push[@]}"
do
    l="$lprefix$pth"
    r="$rprefix$pth"
    echo $l "->" $r
    rsync  -trv  $push_excludes  $l  $host:$r
    echo
done

echo
echo "pulling"
echo
for pth in "${pull[@]}"
do
    l="$lprefix$pth"
    r="$rprefix$pth"
    echo $l "<-" $r
    rsync -trv $host:$r $l
    echo
done

