''' Get a list of names from a csv database.
This module is mainly just a convenient wrapper for
trident/learn/mldata.data_components

NOTE: Make sure you haven't moved around files from their github arrangement!'''
# Zane Markel
# Created 29 SEP 14

import imp
fp, pathname, descr = imp.find_module('mldata', ['../learn/'])
mldata = imp.load_module('mldata', fp, pathname, descr)

def names(csv):
    ''' Given a database csv, extracts the names and returns them '''
    # The '2' index indicates the record names
    return mldata.data_components(mldata.load_data(open(csv)))[2]
