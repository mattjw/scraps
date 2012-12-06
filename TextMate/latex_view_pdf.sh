#!/bin/bash
# Author: Matt J Williams
#
# A better LaTeX View PDF in TextMate. Written as bash script intended for use
# as a TextMate command. 
#
# First attempts to open the PDF corresponding to the currently open .tex file.
# If no PDF is found (e.g., this .tex file is an include in a parent .tex file) 
# the script then attempts to find any PDF in the current .tex file's 
# directory.
#
# The PDF is opened in Preview.

fp_tex=$TM_FILEPATH
fp_pdf=${fp_tex/.tex/.pdf}

# Does the PDF exist?
if [ ! -f "$fp_pdf" ]
then
    # No PDF file. Instead, use first available PDF file 
    # in directory
    fp_pdf=`ls "$TM_DIRECTORY" | grep -i ".pdf"  | head -n 1`
fi

if [ -f "$fp_pdf" ]
then
    open -a /Applications/Preview.app "$fp_pdf"
else
    # Still no PDF?! Give up!
    echo "No PDF found"
fi