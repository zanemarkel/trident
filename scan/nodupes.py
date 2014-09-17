''' This module has functions for ensuring that databases have all
unique files. '''
# Author: Zane Markel
# Created: 17 SEP 2014

import hashlib
import argparse

def hash_file(f, block_size=2**15):
    ''' Takes an open file f and returns the SHA1 hash for it.
    This method will work regardless of file size. '''
    sha = hashlib.sha1()
    while True:
        data = f.read(block_size)
        if not data:
            break
        sha.update(data)
    return sha.hexdigest()

def main():
    clargs = argparse.ArgumentParser('Get the sha1 of a file!')
    clargs.add_argument('fname', type=argparse.FileType('r'), \
        help='The file whose SHA1 you want to compute')
    args = clargs.parse_args()

    print(hash_file(args.fname))

if __name__ == '__main__':
    main()
