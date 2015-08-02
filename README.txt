This is a project that wrangles Open Street Map Data from Stockholm using Mongo DB. 

Explanation of files:
	1. audit_street_names.py is a program I used to look at the street names in the dataset. I used the mapping dictionary and update function in my data.py program. From the command line run as follows:
		python audit_street_names.py FILENAME
	where FILENAME is in XML.

	2. change_cities.py is a program that updates multiple incorrectly named cities. This was run after I put the data into MongoDB.

	3. data.py converts the XML file to JSON. It also shapes the documents to be uploaded into MongoDB. To run the program from the command line:
		python data.py FILENAME
	where FILENAME is the XML file to be converted to json. The output is a file with the same name as FILENAME with a .json ending

	4. example_creator.py makes a sample file. The original file is too big to effectively analyze. To run from command line:
		python example_creator.py stockholm_sweden.osm sample.osm
	This creates a sample.osm file

	5. kattrib_count.py counts the number of times each attribute occurs in a file. To run from command line:
		python kattrib_count.py FILENAME
	where FILENAME is an XML file.

	6. kattrib_analysis.py lists the different value for a specific attribute. To run from command line:
		python kattrib_analysis.py FILENAME 'attribute'
	where FILENAME is an XML file and attribute is an attribute found in k_attributes.txt

	7. mongo.py inputs data from a JSON file into a database. The database is called OpenStreetMap and the collection is Stockholm. To run from command line: 
		python mongo.py FILENAME
	where FILENAME is a JSON file.

	8. tag_counter.py counts the number of each tags in a file. To run from a command file:
		python tag_counter.py FILENAME
	where FILENAME is an XML file. 

Visuals is where all the visuals are. Inside this directory,
	1. get_locations.py takes data from the Stockholm database and given the two arguments outputs a csv file with all the locations. For example, running 
		python get_locations.py 'amenity' 'parking' 
	gives the locations of all the documents with 'amenity' : 'parking' inside of them. 