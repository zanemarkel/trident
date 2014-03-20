#!/bin/bash
find $1 -type f -name malware.zip -exec rm -v {} \;
