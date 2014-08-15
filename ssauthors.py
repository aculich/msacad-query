# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Import basic Python libraries for use in your program: [os.path](http://docs.python.org/2/library/os.path.html) and [ConfigParser](http://docs.python.org/2/library/configparser.html)

# <codecell>

import os.path
import ConfigParser

# <markdowncell>

# An example of reading data from a Google Spreadsheet using the gspread library: http://stackoverflow.com/a/18296318/462302
# 
# First you'll need to install the gspread library on your virtual machine using: `sudo pip install gspread`

# <codecell>

import gspread

# <markdowncell>

# Define `take(n, iterable)` which is a convenience function to limit the amount of output that you print. Useful when you have lots of data that will clutter up your screen!

# <codecell>

from itertools import islice
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

# <markdowncell>

# Read the username and password from the `[google]` section of the `ssauthors.cfg` config file from your virtual machine home directory.

# <codecell>

home = os.path.expanduser("~")
configfile = os.path.join(home, 'ssauthors.cfg')
config = ConfigParser.SafeConfigParser()
config.read(configfile)
username = config.get('google', 'username')
password = config.get('google', 'password')
print username

# <markdowncell>

# Read the docid of the Google Spreadsheet from the config file.

# <codecell>

docid = config.get('docid', 'top100')
client = gspread.login(username, password)
spreadsheet = client.open_by_key(docid)
worksheet = spreadsheet.get_worksheet(0)
print docid

# <markdowncell>

# Add field names to this list to include the column from the Google Spreadsheet in the filtered data output. You should choose one other column in addition to the learning style column. Refer to README.md from the homework assignment.

# <codecell>

fieldnames = ['FIRST','MIDDLE','LAST']
print fieldnames

# <markdowncell>

# Read in ALL rows of data from the Google Spreadsheet, but filter out columns that are not listed in `fieldnames`.

# <codecell>

filtered_data = []
for row in worksheet.get_all_records():
    filtered_data.append({k:v for k,v in row.iteritems() if k in fieldnames})
print "Number of rows: {}".format(len(filtered_data))

# <markdowncell>

# Use the convenience function `take()` to print out only 3 lines from the filtered_data.

# <codecell>

for row in take(3, filtered_data):
    print [row[f] for f in fieldnames]    

# <markdowncell>

# Set up XML parsing for the Microsoft Academic dataset:
# https://datamarket.azure.com/dataset/explore/fd118e3b-6451-4544-bb18-eb01f8970aa5

# <codecell>

from lxml.etree import parse
from urllib2 import urlopen, quote
namespaces = dict([
    ('base',"http://api.datamarket.azure.com/Data.ashx/MRC/MicrosoftAcademic/v1/"),
    ('d',"http://schemas.microsoft.com/ado/2007/08/dataservices"),
    ('m',"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"),
    ('x',"http://www.w3.org/2005/Atom")
])

# <codecell>

def query(author):
    base = 'http://api.datamarket.azure.com/MRC/MicrosoftAcademic/v1/'
    def berkeley_author_query(x): return base + 'Author?$filter=AffiliationID%20eq%20566%20and%20Name%20eq%20%27' + x + '%27'
    doc = parse(urlopen(berkeley_author_query(author)))
    x = doc.xpath('//d:ID/text()', namespaces=namespaces)
    return x

# <codecell>

data = {}
for row in take(100, filtered_data):
    name = [row[f] for f in fieldnames if row[f]]
    author = ' '.join(name)
    ID = query(quote(author))
    if not ID:
        name = [row[f] for f in [x for x in fieldnames if x is not 'MIDDLE'] if row[f]]
        author = ' '.join(name)
        ID = query(quote(author))
    if ID:
        data[ID[0]] = author
        print ID[0], author
    else:
        print "not found:", author

# <codecell>

def papers(author):
    base = 'http://api.datamarket.azure.com/MRC/MicrosoftAcademic/v1/'
    def _query(x): return parse(urlopen(base + 'Paper_Author?$filter=AuthorID%20eq%20' + str(x)))
    doc = _query(author)
    x = doc.xpath('//d:PaperID/text()', namespaces=namespaces)
    for p in x:
        def _query(z): return parse(urlopen(base + 'Paper?$filter=ID%20eq%20' + str(z)))
        doc = _query(p)
        title = doc.xpath('//d:Title/text()', namespaces=namespaces)[0]
        def _query(z): return parse(urlopen(base + 'Paper_Author?$filter=PaperID%20eq%20' + str(z)))
        doc = _query(p)
        names = doc.xpath('//d:Name/text()', namespaces=namespaces)
        print p, title, names
        yield (p, title, names)
[q for q in papers(963417)]

