from pyScraper import *
from pyOnotology import *
import json
def create_structure(table):
	structure = getStructure()
	synonyms = getSynonyms()
	for key in table:
		if isinstance(table[key],dict):
			for key_2 in table[key]:
				for item in table[key][key_2]:					
					if synonyms.has_key(key_2.encode('utf-8')) and item['url'] != None:
						structure[synonyms[key_2.encode('utf-8')][0]][synonyms[key_2.encode('utf-8')][1]] +=  [item['url']] if item['title'] == None else [item]
		elif type(table[key]) is list:
			for key_2 in table[key]:
				if key_2['title'] !=None and synonyms.has_key(key_2['title'].encode('utf-8')) and item['url'] != None:
						structure[synonyms[key_2['title'].encode('utf-8')][0]][synonyms[key_2['title'].encode('utf-8')][1]] +=  [key_2] 
		if key != "content" and type(table[key]) is not list:
				if synonyms.has_key(key.encode('utf-8')):
					structure[synonyms[key.encode('utf-8')][0]][synonyms[key.encode('utf-8')][1]]=table[key.encode('utf-8')]
	return structure

def cleanStructure(structure):
	for key in structure:
		for key_2 in structure[key]:
			if key.encode('utf-8') == "person":
				value = structure[key][key_2][0] if type(structure[key][key_2]) is list else structure[key][key_2] 
				structure[key][key_2] = value['title'].encode('utf-8') if isinstance(value,dict) else value
			else:
				temp = []
				for item in structure[key][key_2]:
					if isinstance(item,dict):
						temp += [item['url'].encode('utf-8')] 
				structure[key][key_2] = temp
	return structure
a = create_structure(politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos"))

print json.dumps(cleanStructure(a), indent=4, sort_keys=True)

