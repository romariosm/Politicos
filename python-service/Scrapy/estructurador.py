from pyScraper import *
from pyOnotology import *
import json
def create_structure(table):
	structure = getStructure()
	synonyms = getSynonyms()

	print table 
	for key in table:
		if isinstance(table[key],dict):
			for key_2 in table[key]:
				if type(table[key][key_2]) is list:
					for item in table[key][key_2]:
						print key_2.encode('utf-8')
						print item #print key_2.encode('utf-8')
						if synonyms.has_key(key_2.encode('utf-8')):
							if item['title'] != None and item['url'] != None:
								structure[synonyms[key_2.encode('utf-8')][0]][synonyms[key_2.encode('utf-8')][1]]=item
							else:
								if item['url'] != None:
									structure[synonyms[key_2.encode('utf-8')][0]][synonyms[key_2.encode('utf-8')][1]]=item['url'].encode('utf-8')
		else:
			if key != "content" and type(table[key]) is not list:
				print key.encode('utf-8')
				if synonyms.has_key(key.encode('utf-8')):
					structure[synonyms[key.encode('utf-8')][0]][synonyms[key.encode('utf-8')][1]]=table[key.encode('utf-8')]
			elif type(table[key]) is list:
				pass
	return structure
				
print create_structure(politic_scrapeTable("https://es.wikipedia.org/wiki/Gustavo_Petro"))
#json.dumps(structure, indent=4, sort_keys=True)

