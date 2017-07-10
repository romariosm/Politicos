from pyScraper import *
from pyOnotology import *

structure = getStructure()
synonyms = getSynonyms()
def create_structure(table):
	for key in table:
		if isinstance(table[key],dict):
			for key_2 in table[key]:
				if isinstance(key_2,dict):
					pass
				else:
					pass
					#print key_2.encode('utf-8')
		else:
			if key != "content" and type(table[key]) is not list:
				if synonyms.has_key(key.encode('utf-8')):
					structure[synonyms[key.encode('utf-8')][0]][synonyms[key.encode('utf-8')][1]]=table[key.encode('utf-8')]
create_structure(politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos"))
print json.dumps(structure, indent=4, sort_keys=True)

