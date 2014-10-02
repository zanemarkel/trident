''' Loads two databases with the same records and combines the features of them into a third database. 
Designed for use with, for example, sigcheck.py 

NOTE: Make sure you haven't moved around files from their github arrangement!'''
# Zane Markel
# 30 SEP 14

# Get mldata
import argparse
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

def fold_dbs(originaldb, newdata):
    ''' Adds the fields in newdata into originaldb. '''

    # Names of the fields
    ofields = originaldb.dtype.names
    nfields = newdata.dtype.names

    retdb = originaldb

    for field in nfields:
        if field not in ofields:
            retdb = mldata.append_feat(retdb, field, newdata[field])

    return retdb

def add_features(originaldb, newdata, outfile):
    ''' originaldb, newdata, and outfile must all be open files.
    This function checks to see if newdata has valid new fields to add to
    originaldb. If it does, then the new database is written to outfile. '''

    odb = mldata.load_data(originaldb)
    ndb = mldata.load_data(newdata)

    if not valid_dbs(odb, ndb):
        raise Exception('The provided databases are not compatible!')

    mldata.save_data(fold_dbs(odb, ndb), outfile)

    return # just for closure

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('database', type=argparse.FileType('r'), \
        help='The original database that you want to add to.')
    argp.add_argument('newdata', type=argparse.FileType('r'), \
        help='The csv with new data fields you want to add to the database.\n\
        Must account for the same files in the same order as the database.')
    argp.add_argument('outfile', type=argparse.FileType('w'), \
        help='The filename of the resultant database.')
    args = argp.parse_args()

    add_features(args.database, args.newdata, args.outfile)

if __name__ == '__main__':
    main()
