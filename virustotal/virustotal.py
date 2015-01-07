""" A module for sending and receiving requests from VirusTotal. """
###############################################################
# Author:       Zane Markel
# Created:      25 MAR 2013
#
# Name:         virustotal
# Description:  A module for sending and receiving requests  
#               from VirusTotal.
#               
###############################################################

import requests
from fractions import Fraction
import re

# This should be removed if this module is ever made public.
APIKEY = '8350d37b16dbdb71f88a480dd9ec1b053142484de45d95596ca193882a70f7bc'

# Plans for testing a generated malware sample:
# encode many times
# gen file of list of md5:filename
# for file in list: !!! Make this concurrent !!!
#   get report on hash
#   sleep(2)
#   if is_report(report): # somebody has tried this, or its a collision
#       md5:filename:detect_rate >> report_exists.txt
#    else:
#        md5:filename > no_report.txt
#  for file in no_report: !!! make this concurrent !!!
#    r = scan(file)
#    print confirmation of submission
#  wait an hour
#  for hash in no_report: !!! make this concurrent !!!
#    get report on hash
#    sleep(2)
#    if is_report(report):
#       md5:filename:detect_rate >> report_exists.txt
#  for line in report_exists:
#      if(detect_rate > PREDETERMINED_THRESHOLD):
#          md5:filename >> needs_more_encoding.txt
#      else:
#          md5:filename >> passed.txt
# All the files in passed.txt are good for scanning
# UPDATE: Make object like [ payload, filename, hash, detection rate (fraction), encoding chain ]
# encoding chain would be like [(shikata-ga-nai, 7), (veil-evasion, 15), ...]

def report(rsrc_hash):
    ''' Reqests a report for a file with the given hash. 
    This is straight from the VirusTotal private API.'''

    params = {'apikey': APIKEY, 'resource': rsrc_hash}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report' \
    , params=params)
    json_response = response.json()

    return json_response

def is_report(response):
    ''' Returns whether or not the response from a report request contains a
    legitimate report. This should be used to tell if a file has been scanned
    before or not. '''

    if(response['response_code'] == 1):
        return True
    elif(response['response_code'] == 0):
        return False
    else:
        return 'WTF %d' % (response['response_code'])

def get_scan_date(response):
    ''' Returns the time of the last scan from a report. '''
    return response['scan_date']

def get_av_names(response):
    ''' Returns the names of the antivirus products used in a report
    as a list. '''
    return [av for av in response['scans']] 

def get_detected(response):
    ''' Returns the bools for the 'detected' values for the antivirus scans
    in a report. '''

    bools = []
    for av in response['scans']:
        bools.append(response['scans'][av]['detected'])

    return bools

def detect_rate(response):
    ''' Returns the percent (as a decimal) of antivirus scans that claimed
    the file in the response is malicious. '''
    detects = get_detected(response)
    return Fraction(sum(detects), len(detects))

def scan(fname):
    ''' Uploads a file for VirusTotal to scan.
    This is straight from the VirusTotal private API.
    
    NOTE: It is good practice to wait 1 hour before requesting a report.'''

    params = {'apikey': APIKEY }
    files = {'file':(fname, open(fname, 'rb'))}
    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', \
    files=files, params=params)
    json_response = response.json()

    return json_response

