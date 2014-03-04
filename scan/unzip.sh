#!/bin/bash
# Created 25 FEB 14
# Recursively unzips files in directory
# Assumes password is "infected"
# arg1 is the directory to search through
find $1 -name "*.zip" | while read filename; do path=${filename%malware.zip}; unzip -P "infected" -o -d "$path" "$filename"; done;
