#! /usr/bin/python
# craig
# katie
# perry
from string import replace

import csv
import datetime
import getopt
import sys
from xml.sax.saxutils import escape


def usage():
    print 'options:  -u <username>'

# Function to clean up values
def cleanValue(value):
    value = escape(value)  # Escapes the below characters that need to be escaped in XML
    # Below handles any instance of double escaped chars
    value = replace(value, "&amp;amp;", "&amp;")
    value = replace(value, "&amp;quot;", "&quot;")
    value = replace(value, "&amp;apos;", "&apos;")
    value = replace(value, "&amp;lt;", "&lt;")
    value = replace(value, "&amp;gt;", "&gt;")
    return value

# Function to clean up keys
def cleanKey(key):
    key = replace(key, '"', '')  # remove double quotes
    key = replace(key, '\'', '')  # remove single quotes
    key = replace(key, ' ', '_')  # replace spaces with underscores
    key = replace(key, '/', '')  # removing slash '/', illegal char in param name in XML
    key = replace(replace(key, ')', ''), '(', '')  # removing brackets ')' and '(', illegal char in param name in XML
    key = replace(key, '#', '') # remove pound sign 
    key = replace(key, '+', '') # remove +
    key = replace(key, '?', '') # remove ?
    key = replace(key, '=', '') # remove =
    key = replace(key, ',', '') # remove ,
    key = replace(key, ':', '') # remove :
    key = replace(key, ';', '') # remove ;
    key = replace(key, '>', '') # remove >
    key = replace(key, '<', '') # remove <
    key = replace(key, '\\', '') # remove '\'
    key = replace(key, '*', '') # remove *
    key = replace(key, '&', '') # remove &
    key = replace(key, '^', '') # remove ^
    key = replace(key, '%', '') # remove %
    key = replace(key, '@', '') # remove @
    key = replace(key, '!', '') # remove !
    key = replace(key, '~', '') # remove ~
    key = replace(key, '.', '') # remove .


    return key


infile = ''
outfile = ''
delimiter = ','
quotechar = '"'
encoding = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:d:q:e:')
except getopt.GetoptError:
    print 'Option Error:'
    usage()
    sys.exit(2)


for (opt, arg) in opts:
    if opt == '-i':
        infile = arg
    elif opt == '-o':
        outfile = arg
    elif opt == '-d':
        delimiter = arg
    elif opt == '-q':
        quotechar = arg
    elif opt == '-h':
        usage()

if not infile:
    print 'Missing -i <input file>'
    sys.exit(2)
if not outfile:
    print 'Missing -o <output file>'
    sys.exit(2)

sys.stderr.write('***' + str(datetime.datetime.now()) + '***\n')

with open(infile, mode='rU') as csvfile:
    with open(outfile, mode='w+') as xmlfile:
        xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xmlfile.write('<products>\n')
        csvreader = csv.DictReader((line.replace('\0', '') for line in csvfile), delimiter=delimiter, quotechar=quotechar)
        for line in csvreader:
            if any(line.values()):
                xmlfile.write("  <product>\n")
                for (key, val) in line.items():
                    # Only bother adding to xml if both Key and Value exist
                    if key and val:
                        # Clean up the key and value
                        cleanedKey = cleanKey(key)
                        cleanedVal = cleanValue(val)
                        xmlfile.write('    <' + cleanedKey + '>' + cleanedVal + '</' + cleanedKey + '>\n')
                xmlfile.write("  </product>\n")
        xmlfile.write('</products>')

sys.stderr.write('***' + str(datetime.datetime.now()) + '***\n')
