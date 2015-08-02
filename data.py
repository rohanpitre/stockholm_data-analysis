#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Shapes the data properly and outputs it to a JSON document
from sys import argv
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

script, file_in = argv

lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
lower = re.compile(r'^([a-z]|_)*$')
valid_address = re.compile(r'^(["addr"]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
MAPPING = { u'V\xe4g': u'v\xe4g',
            u'Gata': u'gata',
			u'All\xe9': u'all\xe9',
			u'V\xe4gen': u'v\xe4gen'
            }

def update_street_name(name, mapping):

    street_words = name.split(' ')
    updated_name = ""
    if street_words[-1] in mapping:
		street_words[-1] = mapping[street_words[-1]]
	
    for word in street_words:
        updated_name += word 
        updated_name += ' '
    
    updated_name = updated_name[:-1]
    return updated_name
	
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        attributes = element.attrib
        
        #add created dictionary to node
        created_dict = {}
        for val in CREATED:
            if val in attributes:
                created_dict[val] = attributes.pop(val)
            else:
                continue
        node['created'] = created_dict

        
        #latitude and longitude array
        pos = []
        if 'lat' in attributes:
            pos.append(float(attributes.pop('lat')))
        
        if 'lon' in attributes:
            pos.append(float(attributes.pop('lon')))
        
        node['pos'] = pos
        
        #adds rest of attributes to node
        node['type'] = element.tag
        for att in attributes:
            node[att] = attributes[att]
        
        #adds information from tags to node
	    seamark_dict = {}
	    address_dict = {}
        for child in element.iter('tag'):
			#converts attribute to unicode
			attribute = child.attrib['v']
			if type(attribute) == type('s'):
				attribute = unicode(attribute, 'utf-8')
			
			if re.search(problemchars, child.attrib['k']):
				print 'PROBLEM CHARACTER FOUND', child.attrib['k']
				continue
			
			#compiles the address dictionary
			elif re.search(valid_address, child.attrib['k']):
				address_key = (child.attrib['k'][5:])
				if address_key == 'street':
					attribute = update_street_name(attribute, MAPPING)
				address_dict[address_key] = attribute
			#building
			elif child.attrib['k'] == 'building':
				if attribute == 'yes':
					attribute = 'building'
				node['building'] = attribute
            #adds other attributes    
			elif re.match(lower_colon, child.attrib['k']):
				attr_words = child.attrib['k'].split(':')
				if attr_words[0] in node:
					if type(node[attr_words[0]]) == type({}):
						node [attr_words[0]][attr_words[1]] = attribute
					elif type(node[attr_words[0]]) == type(u's'):
						temp_dict = {}
						temp_dict[attr_words[0]] = node[attr_words[0]]
						temp_dict[attr_words[1]] = attribute
						node[attr_words[0]] = temp_dict
				else:
					temp_dict = {}
					temp_dict[attr_words[1]] = attribute
					node[attr_words[0]] = temp_dict
			
			#deals with seamark
			elif child.attrib['k'][:7] == 'seamark':
				seamark_dict[child.attrib['k'][8:]] = attribute
			
			elif re.search(lower, child.attrib['k']):
				node[child.attrib['k']] = attribute
        
        #adds the address dictionary
        if len(address_dict) > 0:
            node['address'] = address_dict
			
		#adds the seamark dict
        if len(seamark_dict) > 0:
            node['seamark'] = seamark_dict
        
        #adds the noderefs
        if element.tag == 'way':
            node_ref_list = []
            for child in element.iter('nd'):
                node_ref_list.append(child.attrib['ref'])
            if len(node_ref_list) > 0:
                node['node_refs'] = node_ref_list
        element.clear()
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    process_map(file_in, pretty = False)
