''' A module for handling malware encoding metadata. '''
###############################################################
# Author:       Zane Markel
# Created:      7 JAN 2015
#
# Name:         encoding
# Description:  A module for malware encoding metadata
#
###############################################################

import json
from fractions import Fraction
import re

class Encoding:
    ''' Class that contains all the metadata for an encoded payload.
    Ini'd through known metadata or through a JSON dump in a database.
    Format:
    {'payload':payload, 'filename':fname, 'md5':md5,
    'detects':number_of_avs_detecting_payload, 'tests':number_of_avs_tested,
    'chain':[(encoding, count), (encoding, count), ...]}

    Note that "detects"/"tests" would give the detection rate.
    '''
    def __init__(self, payload='', filename='', md5='', detects=0, tests=0, chain=[]):
        ''' Constructs an Encoding instance with given attributes. '''
        self.payload = payload
        self.filename = filename
        self.md5 = md5
        self.detects = detects
        self.tests = tests
        self.chain = chain

    def detect_rate(self):
        ''' Returns "detects"/"tests" (or 'N/A' if tests == 0) '''
        if self.tests == 0:
            return "N/A"
        return float(self.detects)/float(self.tests)

def loading_encoding(dct):
    ''' takes a line of json dump text and converts it into an Encoding object.
    To be used as the object_hook of json.loads. '''
    if 'payload' in dct:
        return Encoding(dct['payload'], dct['filename'], dct['md5'], \
                dct['detects'], dct['tests'], dct['chain'])
    return dct # this shouldn't happen

class Payload:
    '''Class that contains all the metadata for an encoded payload.
    Initialized though a line in a database.''' 

    def __init__(self, line):
        '''line should be of the form payload:fname:md5:detect_rate:encoding_chain
        e.g. 'cve1337:/tmp/cve1337:fe45...bc:0/55:('shikata-ga-nai,7), (veil-evasion, 15), ...'
        fname should be of the form /absolute/path/.../name'''
        pieces = re.match(r'(.*):(.*):(.*):(.*)/(.*):(.*)$', line)
        if pieces:
            self.payload = pieces.group(1)
            self.fname = pieces.group(2)
            self.md5 = pieces.group(3)
            self.detect_rate = Fraction(pieces.group(4), pieces.group(5))
            # TODO: check for whole numbers e.g. Fraction(1,1) prints as '1'
            # NOT DONE
        else:
            raise Exception("Invalid line {}".format(line))

