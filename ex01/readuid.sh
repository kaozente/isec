#!/bin/bash

STUB="https://hpi-vdb.de/vulndb/isec_task/?uid="
DEFAULTGET="karl.wolf"

if [ -n "$1" ]
# Test whether command-line argument is present (non-empty).
then
  GET=$1
else  
  GET=$DEFAULTGET # Default, if not specified on command-line.
fi 


# fetch all text from personal website
# -s suppresses statistics, so only the website's content is saved
# then filter out everything that looks like a uid: firstname.lastname
# assumption: first names are at least 2, last names at least 3 chars long
# and uids are only composed of lowercase latin letters
curl -s "$STUB$GET" | grep -o -P -e '[a-z]{2,}\.[a-z]{3,}'
