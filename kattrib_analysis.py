from sys import argv
import xml.etree.cElementTree as ET
import pprint

script, FILENAME, attribute = argv

def count_tags(filename):
    tags_counter = {}
    for event, elem in ET.iterparse(filename):
	    if elem.tag == 'tag':
			if elem.attrib['k'] == attribute:
				if elem.attrib['v'] in tags_counter:
					tags_counter[elem.attrib['v']] += 1
				else:
					tags_counter[elem.attrib['v']] = 1
    return tags_counter

		
tags = count_tags(FILENAME)
tags = sorted( ((v,k) for k,v in tags.iteritems()), reverse=True)
pprint.pprint(tags)