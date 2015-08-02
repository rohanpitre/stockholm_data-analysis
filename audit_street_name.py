#!/usr/bin/python
# -*- coding: latin-1 -*-

"""

- audits the OSMFILE and uses the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from sys import argv
import pickle

script, OSMFILE = argv
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


mapping = { u'V\xe4g': u'v\xe4g',
            u'Gata': u'gata',
			u'All\xe9': u'all\xe9',
			u'V\xe4gen': u'v\xe4gen'
            }

def audit_street_type(street_types, street_name):
	street_name = update_name(street_name, mapping)
	street_words = street_name.split(' ')
	if len(street_words) == 3:
		print street_name
		street_type = (street_words)[-1]
		street_types[street_type] += 1

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(int)
    count = 0
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == 'tag':
			if is_street_name(elem):
				if type(elem.attrib['v']) == type('s'):
					street_name = elem.attrib['v'].encode('utf-8')
				else:
					street_name = elem.attrib['v']
				audit_street_type(street_types, street_name)
				count += 1

    print count
    return street_types


def update_name(name, mapping):

    street_words = name.split(' ')
    updated_name = ""
    if street_words[-1] in mapping:
		street_words[-1] = mapping[street_words[-1]]
	
    for word in street_words:
        updated_name += word 
        updated_name += ' '
    
    updated_name = updated_name[:-1]
    return updated_name

def output_dict_to_file(in_dict):
	pprint.pprint(dict(in_dict))

if __name__ == '__main__':
	st_types = audit(OSMFILE)
	#st_types = (dict(st_types))
	#st_types = sorted( ((v,k) for k,v in st_types.iteritems()), reverse=True)
	output_dict_to_file(st_types)
