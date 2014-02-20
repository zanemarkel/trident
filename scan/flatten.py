''' Flattens a tree of directories into a single folder '''
# Zane Markel
# Creation: 20 FEB 14
# flatten.py
# Kudos to mishik from stackoverflow

import os
import sys
from sys import argv
import string
import shutil

#Generate the file paths to traverse, or a single path if a file name was given
def getfiles(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                yield os.path.join(root, name)
    else:
        yield path

def main():
    if(len(argv) != 3):
        print "Need a destination and source!"
        exit(1)
    destination = argv[1]
    fromdir = argv[2]
    print getfiles(fromdir)
    for f in getfiles(fromdir):
        print f
        filename = string.split(f, '/')[-1]
        #if os.path.isfile(destination+filename):
        filename = f.replace(fromdir,"",1).replace("/","_")
        #os.rename(f, destination+filename)
        shutil.copy(f, destination+filename)
    
if __name__ == "__main__":
    main()
