#!/bin/bash

# check if command line argument given
if [ -z "$1" ]
then
	echo "usage: $0 url"
	exit 1
fi

echo "Fetching $1 ..."
# -o to count actual matches rather than lines with a match
# -i to ignore case
# -e to use a regular expression
# -P to use Perl regex syntax for  using non-greedy modifiers to make sure
# 	every a tag is matched on its own

# save list of links to a variable
links=$(curl -Ls $1 | grep -o -P -e '<a.*?href=\".*?\".*?>(.*?)</a>')

# count those links using grep by counting all lines
# kind of a workaround, but as wc -l is not allowed and using
# the -c flag on grep in the first place doesn't work as it counts
# lines containing on or more matches rather than the total number of
# matches
no=$(echo "$links" | grep -c 'a')
echo "Found $no links!"

# a list of all link tags are is still saved and can be used for further purposes
