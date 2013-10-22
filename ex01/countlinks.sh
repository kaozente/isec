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
# -c to output number of matches instead of printing matches
# -e to use a regular expression
# -P to use Perl regex syntax for  using non-greedy modifiers to make sure
# 	every a tag is matched on its own

# save list of links to a variable
links=$(curl -s $1 | grep -o -P -e '<a.*?href=\".*?\".*?>(.*?)</a>')

# print list of links
echo 'List of links:'
echo "$links"
