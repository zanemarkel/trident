""" Scans a directory for pe32 file header data. Outputs a CSV. """
###############################################################
# Author:       Zane Markel
# Created:      23 APR 2013
#
# Name:         pescanner
# Description:  given a directory, this program will scan for executables and
#               snatch the pe32 file header details from them. It will then
#               organize the data into a CSV.
#
#               Most attributes are raw data which can be computed into better
#               ML attributes later. However, I had to make aggregate boolean 
#               attributes for the sections attributes, because each example
#               has a variable number of sections yet must have the same number
#               of attributes.
#
#               Magic numbers in attribute data:
#               BaseOfData not found -> -1
#               Unknown (sub)language -> lang bools set to -1
###############################################################
# TODO: add all the attribute checks 
###############################################################
# NOTE: to add an attribute, you must update the following:
#       1. grab the attribute from the pe object
#       2. append the attribute to pe_list in the pe_analysis function
#       3. update the CSV header line appropriately
###############################################################

import pefile # the bulk of the work will be done with this
from os import walk # used to grab the directory contents
from os.path import join, exists, getsize
import optparse # for parsing command line options
import sys
import datetime

###############################################################
# CONSTANTS ####################
LOW_ENTROPY = 1
HIGH_ENTROPY = 7


###############################################################
# FUNCTIONS ####################

def get_all_files(root):
    """This function will go through the subdirectories recursively"""
    filelist = []
    for root, sub, files in walk(root):
        for filename in files:
            filelist.append( join(root, filename) )
    return filelist

def lang_bools(pe):
    """Scours the resource directory of a PE32 file for language information.
    Returns four booleans that Yonts argued might make good malware indicators.
    The booleans are: Language=0, Language>127, SubLanguage=0, SubLanguage=2"""

    ret = [0, 0, 0, 0]

    # Getting to the language attributes requires a lot of digging
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if hasattr(resource_type, 'directory'):
                for resource_id in resource_type.directory.entries:
                    if hasattr(resource_id, 'directory'):
                        for resource_lang in resource_id.directory.entries:
                            lang = pefile.LANG.get(resource_lang.data.lang, \
                            '*unknown*')
                            sublang = pefile.get_sublang_name_for_lang( \
                            resource_lang.data.lang, resource_lang.data.sublang)

                            # Here we check if we need to set any bools to true
                            try:
                                if(pefile.LANG[lang] == 0):
                                    ret[0] = 1
                                if(pefile.LANG[lang] > 127):
                                    ret[1] = 1
                            except KeyError:
                                print 'KeyError!'
                                ret[0] = -1
                                ret[1] = -1
                            try:
                                if(pefile.SUBLANG[sublang] == 0):
                                    ret[2] = 1
                                if(pefile.SUBLANG[sublang] == 2):
                                    ret[3] = 1
                            except KeyError:
                                print 'KeyError!'
                                ret[2] = -1
                                ret[3] = -1
    return ret                            


def header_line():
    """
    Returns a CSV column header line
    Update this whenever you add attributes to be measured
    """
    return 'Name, NumberOfSections, Year, \
    PointerToSymbolTable, NumberOfSymbols, BYTES_REVERSED_LO, \
    BYTES_REVERSED_HI, RELOCS_STRIPPED, LOCAL_SYMS_STRIPPED, \
    LINE_NUM_STRIPPED, MajorLinkerVersion, MinorLinkerVersion, \
    MajorOperatingSystemVersion, MinorOperatingSystemVersion, \
    MajorImageVersion, MinorImageVersion, SizeOfCode, \
    SizeOfInitializedData, SizeOfImage, SizeOfHeaders, \
    SizeOfStackReserve, SizeOfStackCommit, SizeOfHeapReserve, \
    SizeOfHeapCommit, AddressOfEntryPoint, BaseOfCode, BaseOfData, \
    Reserved1, LoaderFlags, NumberOfRvaAndSizes, RawSize==0, \
    VirtualLessThanRaw, VirtualWayGreaterThanRaw, NumRelocation!==0, \
    NumLinenums!=0, PointerToRawData==0, PointerToRelocations!=0, \
    PointerToLinenumbers!=0, LowEntropy, HighEntropy, Language=0, \
    Language>127, SubLang=0, SubLang=2, .rsrc size, sample size, \
    RaisedException, isMalware\n'

def pe_analysis(pathname, ftype):
    """
    Returns a string with attribute data for the paricular pe file
    Should be tried and caught
    Return format should follow that of header_line()
    """
    # Grab the PE data
    pe = pefile.PE(pathname)

    # Organize the data into a list
    pe_list = []

    raised_exception = 0    

    # Name
    pe_list.append(pathname)

    # Number of sections
    pe_list.append( pe.FILE_HEADER.NumberOfSections )

    # Year
    rawDate = pe.FILE_HEADER.TimeDateStamp
    pe_list.append(datetime.datetime.fromtimestamp(int(rawDate)).strftime('%Y'))

    # Pointer to symbol table and number of symbols
    pe_list.append( pe.FILE_HEADER.PointerToSymbolTable )
    pe_list.append( pe.FILE_HEADER.NumberOfSymbols )

    # Characteristics flags
    pe_list.append( int(pe.FILE_HEADER.IMAGE_FILE_BYTES_REVERSED_LO) )
    pe_list.append( int(pe.FILE_HEADER.IMAGE_FILE_BYTES_REVERSED_HI) )
    pe_list.append( int(pe.FILE_HEADER.IMAGE_FILE_RELOCS_STRIPPED) )
    pe_list.append( int(pe.FILE_HEADER.IMAGE_FILE_LOCAL_SYMS_STRIPPED) )
    pe_list.append( int(pe.FILE_HEADER.IMAGE_FILE_LINE_NUMS_STRIPPED) )

    # OptionalHeader Version Attributes
    pe_list.append( pe.OPTIONAL_HEADER.MajorLinkerVersion )
    pe_list.append( pe.OPTIONAL_HEADER.MinorLinkerVersion )
    pe_list.append( pe.OPTIONAL_HEADER.MajorOperatingSystemVersion )
    pe_list.append( pe.OPTIONAL_HEADER.MinorOperatingSystemVersion )
    pe_list.append( pe.OPTIONAL_HEADER.MajorImageVersion )
    pe_list.append( pe.OPTIONAL_HEADER.MinorImageVersion )

    # OptionalHeader Size Attributes
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfCode )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfInitializedData )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfImage )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfHeaders )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfStackReserve )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfStackCommit )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfHeapReserve )
    pe_list.append( pe.OPTIONAL_HEADER.SizeOfHeapCommit )

    # OptionalHeader Location Attributes
    pe_list.append( pe.OPTIONAL_HEADER.AddressOfEntryPoint )
    pe_list.append( pe.OPTIONAL_HEADER.BaseOfCode )
    try:
        pe_list.append( pe.OPTIONAL_HEADER.BaseOfData )
    except AttributeError:
        raised_exception = 1
        pe_list.append( -1 ) # BaseOfData not found

    # OptionalHeader Misc Attributes
    pe_list.append( pe.OPTIONAL_HEADER.Reserved1 )
    pe_list.append( pe.OPTIONAL_HEADER.LoaderFlags )
    pe_list.append( pe.OPTIONAL_HEADER.NumberOfRvaAndSizes )
    
    # Section information
    raw_size_bool = 0           # RawSize == 0
    virtual_lt_raw_bool = 0     # VirtualSize > RawSize
    virtual_way_gt_raw_bool = 0 # VirtualSize/RawSize > 10
    num_relocations_bool = 0    # Number of Relocations != 0
    num_line_nums_bool = 0      # Number of line-numbers != 0
    ptr_raw_bool = 0            # PointerToRawData == 0
    ptr_reloc_bool = 0          # PointerToRelocation != 0
    ptr_line_nums_bool = 0      # PointerToLinenumbers != 0
    sml_entropy_bool = 0        # Entropy < 1
    large_entropy_bool = 0      # Entropy > 7
    rsrc_size = -1                  # Resource Size -- will be used later
    for section in pe.sections:
        if(section.SizeOfRawData == 0):
            raw_size_bool = 1
        if(section.Misc_VirtualSize < section.SizeOfRawData):
            virtual_lt_raw_bool = 1
        if(section.SizeOfRawData == 0 or \
            (section.Misc_VirtualSize / section.SizeOfRawData > 10)):
            virtual_way_gt_raw_bool = 1
        if(section.NumberOfRelocations != 0):
            num_relocations_bool = 1
        if(section.NumberOfLinenumbers != 0):
            num_line_nums_bool = 1
        if(section.PointerToRawData == 0):
            ptr_raw_bool = 1
        if(section.PointerToRelocations != 0):
            ptr_reloc_bool = 1
        if(section.PointerToLinenumbers != 0):
            ptr_line_nums_bool = 1
        entropy = section.get_entropy() # This one really slows down the program
        if(entropy < LOW_ENTROPY):
            sml_entropy_bool = 1
        if(entropy > HIGH_ENTROPY):
            large_entropy_bool = 1
        if( '.rsrc' in section.Name ): 
            rsrc_size = section.SizeOfRawData 
    pe_list.append(raw_size_bool)
    pe_list.append(virtual_lt_raw_bool)
    pe_list.append(virtual_way_gt_raw_bool)
    pe_list.append(num_relocations_bool)
    pe_list.append(num_line_nums_bool)
    pe_list.append(ptr_raw_bool)
    pe_list.append(ptr_reloc_bool)
    pe_list.append(ptr_line_nums_bool)
    pe_list.append(sml_entropy_bool)
    pe_list.append(large_entropy_bool)

    # PE resource Indicators
    # This checks the resource file languages for anything abnormal
    langs = lang_bools(pe)
    for this_bool in langs:
        if(this_bool is -1):
            raised_exception = 1
        pe_list.append(this_bool)
    
    # Resource size and the actual sample size (for comparison)
    pe_list.append(rsrc_size)
    pe_list.append(getsize(pathname))

    # RaisedException indicates if anything in the scan caused an exception to be raised
    pe_list.append(raised_exception)

    # isMalware
    if(ftype == 'malware'):
        pe_list.append(1)
    elif(ftype == 'clean'):
        pe_list.append(0)
    else: # ftype should be malware or clean
        pe_list.append(-1)

    # Create a line of CSV from the data
    pe_list.reverse() # To pop from the other side
    csv_str = ('{}'.format(pe_list.pop()) )
    while(pe_list):
        csv_str += (', {}'.format(pe_list.pop()) )

    return csv_str
    

###############################################################
# MAIN #########################

def main():
    # Handle options
    parser = optparse.OptionParser("usage: %prog -d <directory>")
    parser.add_option('-d', dest='directory', type='string', \
            help='the directory you want to scan')
    parser.add_option('-o', dest='output', type='string', \
            help='the name of the output file')
    parser.add_option('-t', dest='ftype', type='string', \
            help='the type of file: either malware or clean')
    parser.add_option('-a', action='store_true', dest='append', default=False, \
            help='append to an existing file rather than overwrite it')
    (options, args) = parser.parse_args()
    if(options.directory == None):
        options.directory = raw_input("What directory do you want to scan? ")
    if(options.output == None):
        options.output = raw_input("Name of output file? ")
    while(options.ftype != 'malware' and options.ftype != 'clean'):
        options.ftype = raw_input("Are these files 'malware' or 'clean' ")


    # Open a file for writing
    if(not options.append):
        outfile = open(options.output, 'w')
        # Write the header data
        outfile.write(header_line())

    else: # Simply append to the file
        if(exists(options.output)):
            outfile = open(options.output, 'a')
        else:
            print '%s does not exist. Use an existing file if you wish to\
            append.' % (options.output)
            sys.exit(1)

    # Get the list of files to scan
    filelist = get_all_files(options.directory)

    # run the pe_analysis on every file in filelist
    for filename in filelist:
        try:
            result = pe_analysis(filename, options.ftype) 
            outfile.write('%s\n' % (result))
            print 'Examined %s' % (filename)
        except pefile.PEFormatError as pfe:
            print '%s is not a pefile: %s' % (filename, str(pfe))           
        except UnboundLocalError as ule:
            print 'Problems with %s: %s' % (filename, str(ule))
        except AttributeError as ae:
            print 'Problems with %s: %s' % (filename, str(ae))


if __name__ == '__main__':
    main()

'''
Here is the list of attributes checks in the Yonts paper.
Checks for all of these should all be added eventually.

A.1.1FileHeader
NumberOfSections            DONE
TimeDateStamp               DONE
PointerToSymbolTable        DONE
NumberOfSymbols             DONE
Machine                     NOT USEFUL - Yonts
Characteristics             DONE
SizeOfOptionalHeader        NOT USEFUL - Yonts

A.1.2Sections
Name
VirtualAddress              NOTE USEFUL - Yonts
VirtualSize                 DONE
RawSize                     DONE
PtrRawData                  DONE
Characteristics
Misc
Misc_Phy_Addr               NOTE USEFUL - Yonts
PtrRelocs                   DONE
PtrLineNums                 DONE
NumRelocs                   DONE
NumLineNums                 DONE
Entropy                     DONE

A.1.3Resources
DateMinor
Name
Subname
Language
Sub3Language
CodePage                    DONE
RVA
Size
Type

A.1.4OptionalHeader 
AddressOfEntryPoint         DONE
MinorOperatingSystemVersion DONE
BaseOfCode                  DONE
MinorSubsystemVersion       NOT USEFUL - Yonts
BaseOfData                  DONE
NumberOfRvaAndSizes         DONE
CheckSum                    NOT USEFUL - Yonts 
SectionAlignment            NOT USEFUL - Yonts
DllCharacteristics          NOT USEFUL - Yonts
SizeOfCode                  DONE
FileAlignment               NOT USEFUL - Yonts
SizeOfHeaders               DONE
ImageBase                   DONE
SizeOfHeapCommit            DONE
LoaderFlags                 DONE
SizeOfHeapReserve           DONE
Magic                       NOT USEFUL - Yonts
SizeOfImage                 DONE
MajorImageVersion           DONE
SizeOfInitializedData       DONE
MajorLinkerVersion          DONE
SizeOfStackCommit           DONE
MajorOperatingSystemVersion DONE
SizeOfStackReserve          DONE
MajorSubsystemVersion       NOT USEFUL - Yonts
SizeOfUninitializedData     DONE
MinorImageVersion           DONE
Subsystem                   NOT USEFUL - Yonts
MinorLinkerVersion          DONE
Reserved1                   DONE
'''
