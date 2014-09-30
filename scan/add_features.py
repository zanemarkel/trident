''' Loads two databases with the same records and combines the features of them into a third database. 
Designed for use with, for example, sigcheck.py 

NOTE: Make sure you haven't moved around files from their github arrangement!'''
# Zane Markel
# 30 SEP 14

# Get mldata
import imp
fp, pathname, descr = imp.find_module('mldata', ['../learn/'])
mldata = imp.load_module('mldata', fp, pathname, descr)

def record_equivalence(data1, data2):
    ''' Checks whether the databases have equivalent record names. '''
    for these in zip(data1['Name'], data2['Name']):
        if these[0] != these[1]:
            return False
    return True

def valid_dbs(originaldb, newdata):
    ''' Checks whether the fields in newdata can properly be added to originaldb
    To be valid, originaldb must have isMalware and Name fields. Also, newdata
    must have Name. Finally, both databases must have records pertaining to the
    same names in the same order.'''

    ofields = originaldb.dtype.names
    nfields = newdata.dtype.names

    if ('isMalware' not in ofields) or ('Name' not in ofields) or \
       ('Name' not in nfields):
        return False

    return record_equivalence(originaldb, newdata)

# TODO: load data -> valid_dbs -> add fields from newdata not in originaldb
