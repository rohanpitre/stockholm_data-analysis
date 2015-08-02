import xml.etree.cElementTree as ET
import pprint
from sys import argv
## counts the number of each tag in the Stockholm data set
## input is the Stockholm osm file
## output is a dictionary containing all the tags as keys 
## and the number of times they appear in the dataset as 
## values

script, FILENAME = argv

def count_tags(filename):
    tags_counter = {}
    for event, elem in ET.iterparse(filename):
	    if elem.tag in tags_counter:
			tags_counter[elem.tag] += 1
	    else:
		    tags_counter[elem.tag] = 1
    return tags_counter

		
tags = count_tags(FILENAME)
pprint.pprint(tags)