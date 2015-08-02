#updates cities in MongoDB

import pymongo
from pymongo import MongoClient

client = MongoClient()

db = client.OpenStreetMap


city_mapping = {
	u'VENDELS\u00D6' : u'Vendels\u00F6',
	u'TUMBA' : u'Tumba',
	u'GR\u00D6DINGE' : u'Gr\u00F6dinge',
	u's\u00F6dert\u00E4lje' : u'S\u00F6dert\u00E4lje',
	u'H\u00C4GERSTEN' : u'H\u00E4gersten',
	u'V\u00C4STERLJUNG' : u'V\u00E4sterljung',
	u'SP\u00C5NGA' : u'Sp\u00E5nga',
	u'STOCKHOLM' : u'Stockholm',
	u'BROMMA' : u'Bromma',
	u'HANINGE' : u'Haninge',
	u'huddinge' : u'Huddinge',
	u'Hudding' : u'Huddinge',
	u'TUNGELSTA' : u'Tungelsta',
	u'SK\u00C4RHOLMEN' : u'Sk\u00E4rholmen',
	u'v\u00E4sterhaninge' : u'V\u00E4sterhaninge',
	u'T\u00C4BY' : u'T\u00E4by',
	u'SALTSJ\u00D6BADEN' : u'Saltsj\u00F6baden',
	u'v\u00E4llingby' : u'V\u00E4llingby',
	u'nyn\u00E4shamn' : u'Nyn\u00E4shamn',
	u'h\u00E4gersten' : u'H\u00E4gersten',
	u'\u00C4LVSJ\u00D6' : u'\u00C4lvsj\u00F6', 
	u'SK\u00C4RHOLMEN' : u'Sk\u00E4rholmen',
	u'H\u00C4GERSTEN\n' : u'H\u00E4gersten',
}

for city in city_mapping:
	try:
		db.Stockholm.update({"address.city" : city}, 
		{"$set": {"address.city": city_mapping[city]}},
		multi = True)
	except:
		print 'Failed to add', city
