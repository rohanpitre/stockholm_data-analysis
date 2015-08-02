from pymongo import MongoClient
import pymongo
from sys import argv
import pandas 
import numpy

client = MongoClient()
db = client.OpenStreetMap

script, attribute, value = argv

loc_info = db.Stockholm.aggregate(
	[
		{"$match" : {attribute : value}},
		{"$project" : {'_id': 0, 'pos' : 1}},
		{"$sort" : {"pos" : -1}}
	]
	)

lat = []
lon = []

for point in loc_info:
	if point['pos'] == []:
		break
	lat.append(point['pos'][0])
	lon.append(point['pos'][1])

df = {'lat' : pandas.Series(lat), 'lon' : pandas.Series(lon)}
df = pandas.DataFrame(df)

filename = value + '.csv'
df.to_csv(filename)




