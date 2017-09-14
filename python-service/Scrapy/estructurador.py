from pyScraper import *
from pyOnotology import *
import json
import cypherMaker as CM

def create_structure(table):
	structure = getStructure()
	synonyms = getSynonyms()
	for key in table:
		if isinstance(table[key],dict):
			if "#" in key:
				if synonyms.has_key(key.encode('utf-8').split("#")[0].strip()):
					structure[synonyms[key.encode('utf-8').split("#")[0].strip()][0]][synonyms[key.encode('utf-8').split("#")[0].strip()][1]].append(key)
			else:				
				for key_2 in table[key]:				
					for item in table[key][key_2]:
						if synonyms.has_key(key_2.encode('utf-8')) and item['url'] != None:
							structure[synonyms[key_2.encode('utf-8')][0]][synonyms[key_2.encode('utf-8')][1]] +=  [item['url']] if item['title'] == None else [item]
		elif type(table[key]) is list:
			for key_2 in table[key]:
				if key_2['title'] !=None and synonyms.has_key(key_2['title'].encode('utf-8')) and key_2['url'] != None:
					structure[synonyms[key_2['title'].encode('utf-8')][0]][synonyms[key_2['title'].encode('utf-8')][1]] +=  [key_2] 
		if key != "content" and type(table[key]) is not list:
				if synonyms.has_key(key.encode('utf-8')):
					structure[synonyms[key.encode('utf-8')][0]][synonyms[key.encode('utf-8')][1]]=table[key.encode('utf-8')]
	return structure

def create_structure_organization(table):
	structure = getStructureOrg()
	synonyms = getSy_Org()
	for key in table:
		if isinstance(table[key],dict):
			for key_2 in table[key]:
				if type(table[key][key_2]) is list:
					for value in table[key][key_2]:
						if value['title'] is not None:
							if synonyms.has_key(key_2.encode('utf-8')):
								structure[synonyms[key_2.encode('utf-8')]] = value['title'].encode('utf-8')
		elif type(table[key]) is not list:
			if synonyms.has_key(key.encode('utf-8')):
				structure[synonyms[key.encode('utf-8')]] = table[key].encode('utf-8')
	return structure

def create_structure_institution(table):
	structure = getStructureInst()
	synonyms = getSy_Inst()
	for key in table:
		if isinstance(table[key],dict):
			for key_2 in table[key]:
				if type(table[key][key_2]) is list:
					for value in table[key][key_2]:
						if value['title'] is not None:
							if synonyms.has_key(key_2.encode('utf-8')):
								structure[synonyms[key_2.encode('utf-8')]] = value['title'].encode('utf-8')
		elif type(table[key]) is not list:
			if synonyms.has_key(key.encode('utf-8')):
				structure[synonyms[key.encode('utf-8')]] = table[key].encode('utf-8')
	return structure

def create_structure_party(table):
	structure = getStructureParty()
	synonyms = getSy_Party()
	for item in table:
		if synonyms.has_key(item.encode('utf-8')):
			structure[synonyms[item.encode('utf-8')]] = table[item]
	return structure

def create_structure_site(table):
	structure = getStructureSite()
	synonyms = getSy_Site()
	for item in table:
		if synonyms.has_key(item.encode('utf-8')):
			structure[synonyms[item.encode('utf-8')]] = table[item]
	return structure	

def cleanStructure(structure):
	for key in structure:
		for key_2 in structure[key]:
			if key.encode('utf-8') == "person":
				value = (structure[key][key_2][0] if len(structure[key][key_2])>0 else "" ) if type(structure[key][key_2]) is list else structure[key][key_2] 
				structure[key][key_2] = value['title'].encode('utf-8') if isinstance(value,dict) else value
			#elif 
			#	pass #print structure[key][key_2]
			else:
				temp = []
				for item in structure[key][key_2]:
					if isinstance(item,dict):
						temp += [item['url'].encode('utf-8')]
					else:
						temp += [item.encode('utf-8')] 
				if key.encode('utf-8') == "party":
					partys = getParty()
					subTemp = []
					for link in temp:
						if partys.has_key(link):
							subTemp.append(link.encode('utf-8'))
					temp = subTemp
				structure[key][key_2] = temp
	return structure

def searchFamily(structure,recorded,newFamily):
	for item in structure['family']:
		for link in structure['family'][item]:
			if link not in recorded:
				recorded.append(link)
				createTree(link,recorded,newFamily)

def createTree(link,recorded,newFamily):
	politic = politic_scrapeTable(link)
	a = create_structure(politic)
	c = cleanStructure(a)
	if savePerson(c) == True:
		newFamily += [politic]
	relatedFamily(c,recorded,newFamily)
	relateOrganizationsAcademic(c)
	relateParty(c)
	relateOrganizationsLaboral(c)
	relatePlaces(c)		
	searchFamily(c,recorded,newFamily)

def savePerson(structure):
	return False if CM.exists('person',{'Url':structure['person']['Url']}) else CM.create('person',structure['person']) 

def saveNode(structure,label):
	return True if CM.exists(label,{'Url':structure['Url']}) else CM.create(label,structure) 

def relatedFamily(structure,stored=[],newFamily=[]):
	family = newFamily
	for key in structure['family']:
		for person in structure['family'][key]:
			#print key +' -> '+ person
			if not CM.exists('person',{'Url':person}):
				scrap_person = politic_scrapeTable(person)
				family += [scrap_person]
				clean_person = cleanStructure(create_structure(scrap_person))
				savePerson(clean_person)
			if not CM.existsRelation('family',{'type':key} ,'person',{'Url':structure['person']['Url']},'person',{'Url':person}):
				CM.makeRelation('family',{'type':key} ,'person',{'Url':structure['person']['Url']},'person',{'Url':person})
	searchFamily(structure,stored,family)			
	return family

def relateOrganizationsLaboral(structure):
	noCreated = []
	array = structure['organization']['laboral']
	relation = 'worksAt'
	node = 'organization'
	entities = getEntities()
	for key in array:
		if not CM.exists(node,{'Url':entities[key.split('#')[0].strip()]}):
			scrap = politic_scrapeTable(entities[key.split('#')[0].strip()])			
			saveNode(create_structure_organization(scrap),node)
			noCreated += [scrap]
		if not CM.existsRelation(relation,{} ,'person',{'Url':structure['person']['Url']},node,{'Url':entities[key.split('#')[0].strip()]}):
			properties = {}
			properties['Cargo'] = key.split('#')[0].strip()
			properties['Inicio'] = key.split('#')[1].split('-')[0].strip()
			dateInicio = properties['Inicio'].replace('Desde el ','').split(' de ')
			properties['InicioJul'] = str(gregToJul(dateInicio[0],dateInicio[1],dateInicio[2]))
			properties['Fin'] = key.split('#')[1].split('-')[1].strip() if len(key.split('#')[1].split('-'))>1 else "" 
			if properties['Fin'] != "":
				dateFin = properties['Fin'].split(' de ')
				properties['FinJul'] = str(gregToJul(dateFin[0],dateFin[1],dateFin[2]))
			print properties			
			CM.makeRelation(relation,properties,'person',{'Url':structure['person']['Url']},node,{'Url':entities[key.split('#')[0].strip()]})
	return noCreated

def relateParty(structure):
	noCreated = []
	array = structure['party']['name']
	relation = 'belongsTo'
	node = 'party'	
	for key in array:
		if not CM.exists(node,{'Url':key}):
			party = politic_scrapeTable(key)
			scrap = create_structure_party(party)	
			saveNode(scrap,node)
			noCreated += [scrap]			
		if not CM.existsRelation(relation,{} ,'person',{'Url':structure['person']['Url']},node,{'Url':key}):
			CM.makeRelation(relation,{} ,'person',{'Url':structure['person']['Url']},node,{'Url':key})
	return noCreated

def relateOrganizationsAcademic(structure):
	noCreated = []
	array = structure['organization']['academic']
	relation = 'studiedAt'
	node = 'institution'		
	for key in array:	
		if not CM.exists('organization',{'Url':key}):
			inst = politic_scrapeTable(key)
			scrap = create_structure_institution(inst)
			saveNode(scrap,node)
			noCreated += [scrap]			
		if not CM.existsRelation(relation,{} ,'person',{'Url':structure['person']['Url']},node,{'Url':key}):
			CM.makeRelation(relation,{} ,'person',{'Url':structure['person']['Url']},node,{'Url':key})
	return noCreated

def getPersonalFamiliarInfo(url,level):
	return CM.getPersonalFamiliarInfo({'Url':url},level)

def relatePlaces(structure):
	array = structure['site']['birth']
	dic = {}
	site_no_registered = []
	for cosa in array:
		dom = cosa.split("/")
		valor = dom[len(dom)-1]
		if valor.split("_")[0].isdigit():
			if len(valor.split("_")) > 1:
				dic['day'] = valor.split("_")[0] # Mejorar esto, no creo que funcione para todos 
				dic['moth'] = valor.split("_")[2]
			else:
				dic['year'] = valor
			array = [x for x in array if x != cosa]
	for site in array:
		if not CM.exists('Site',{'Url':site}):
			scrap_site = politic_scrapeTable(site)
			site_no_registered += [scrap_site]
			saveNode(create_structure_site(scrap_site),"site")
		if not CM.existsRelation('born',{} ,'person',{'Url':structure['person']['Url']},'site',{'Url':site}):
			CM.makeRelation('born',dic ,'person',{'Url':structure['person']['Url']},'site',{'Url':site})


def gregToJul(day,month,year):
	day,month,year = int(day),Representsmonth(month),int(year)
	if (month > 2):
		month = month - 3
	else:
		month = month + 9
		year = year - 1
	cen = year / 100
	dec = year - 100 * cen
	return (146097 * cen) / 4 + (1461 * dec) / 4 + (153 * month + 2) / 5 + day + 1721119

def Representsmonth(s):
    try: 
        return int(s)
    except ValueError:
        return {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
		'noviembre': 11,
		'diciembre': 12,
    	}[s]

print createTree("https://es.wikipedia.org/wiki/Juan_Manuel_Santos",[],[])