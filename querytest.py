# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from lxml.etree import parse
from lxml import objectify
from urllib2 import urlopen

# <codecell>

namespaces = [
    ('base',"http://api.datamarket.azure.com/Data.ashx/MRC/MicrosoftAcademic/v1/"),
    ('d',"http://schemas.microsoft.com/ado/2007/08/dataservices"),
    ('m',"http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"),
    ('x',"http://www.w3.org/2005/Atom")
]

n = dict(namespaces)

# <codecell>

base = 'http://api.datamarket.azure.com/MRC/MicrosoftAcademic/v1/'
author            = base + 'Author?$filter=AffiliationID%20eq%20566%20and%20Name%20eq%20%27junko%20habu%27'
doc = parse(urlopen(author))
x = doc.xpath('//d:ID/text()', namespaces=n)
print x

# <codecell>

paper_list        = base + 'Paper_Author?$filter=AuthorID%20eq%20' + x[0]
doc = parse(urlopen(paper_list))
x = doc.xpath('//d:PaperID/text()', namespaces=n)
print x

# <codecell>

paper             = base + 'Paper?$filter=ID%20eq%20' + x[0]
doc = parse(urlopen(paper))
x = doc.xpath('//d:ID/text()', namespaces=n)
print x

# <codecell>

coauthor_list     = base + 'Paper_Author?$filter=PaperID%20eq%20' + x[0]
doc = parse(urlopen(coauthor_list))
x = doc.xpath('//d:AuthorID/text()', namespaces=n)
print x

# <codecell>

coauthor           = base + 'Author?$filter=ID%20eq%20' + x[1]
doc = parse(urlopen(coauthor))
x = doc.xpath('//d:ID/text()', namespaces=n)
print x

# <codecell>

coauthor_affiliation = base + 'Author?$filter=ID%20eq%20' + x[0]
doc = parse(urlopen(coauthor_affiliation))
x = doc.xpath('//d:AffiliationID/text()', namespaces=n)
print x

# <codecell>

other_affiliation = base + 'Affiliation?$filter=ID%20eq%20' + x[0]
doc = parse(urlopen(other_affiliation))
x = doc.xpath('//d:OfficialName/text()', namespaces=n)
print x

# <codecell>

author

