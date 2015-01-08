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

class Encoding():
    ''' Class that contains all the metadata for an encoded payload.
    Ini'd through known metadata or through a JSON dump in a database.
    Format:
    {'payload':payload, 'filename':fname, 'md5':md5,
    'detects':number_of_avs_detecting_payload, 'tests':number_of_avs_tested,
    'chain':[[encoding, count], [encoding, count], ...]}

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

    def to_str(self):
        ''' Returns a json-dump string of the object.'''
        return json.dumps(self.__dict__)

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

def load_line(line):
    ''' wrapper for loading_encoding that alleviates need to call any json
    function. '''
    return json.loads(line.strip(), object_hook=loading_encoding)
