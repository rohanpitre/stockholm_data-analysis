 # -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
from sys import argv
import json

script, FILENAME = argv

client = MongoClient('localhost', 27017)
db = client.OpenStreetMap
stockholm = db.Stockholm

def insert_doc (filename) :

	counter = 0
	with open(filename, 'r') as f:
		for line in f:
			try:
				stockholm.insert(json.loads(line))
				counter += 1
			except ValueError as e:  
				print "Value Error: ", e  
			
			if counter % 1000 == 0:
				print counter, " lines added"
	
	print
	print counter, "records added"

insert_doc(FILENAME)