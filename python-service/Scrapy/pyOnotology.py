import json
import Libraries.pyRedis as redis
import Libraries.FileManager as fm

# -*- coding: utf-8 -*-
def loadCategories():
	try:     
		with fm.readFile("categorias.json") as file:
			for line in file:
				ajson = json.loads(line)
				print "sadd categoria " + ajson["category"].encode("utf-8")
				def function(redisClient):					
					return "Registros insertados: " + str(redisClient.sadd("categoria",u"Categor\u00eda:"+ajson["category"]))
				print(redis.sendRedis(function))
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de las categorias: \n" + str(ex))
def loadSynonyms(): 
	try:     

		with fm.readFile("cargue_ontologia.txt",fm.path['loads']) as file:
			def function(redisClient):
				for line in file:
					ajson = json.loads(line)
					for key in ajson:
						for key_2 in ajson[key]:
							for item in ajson[key][key_2]:
								print "set "+"CLAVE="+"sinonimo:"+item.encode('utf-8') + "  VALOR=" +key.encode('utf-8')+":"+key_2.encode('utf-8')
								print "Registros insertados: " + str(redisClient.set("sinonimo:"+item.encode('utf-8'),key.encode('utf-8')+":"+key_2.encode('utf-8')))
						print
			redis.sendRedis(function)	
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de sinonimos: \n" + str(ex))
def loadSynonyms_party(): 
	try:     
		with fm.readFile("cargue_party.txt",fm.path['loads']) as file:
			def function(redisClient):
				for line in file:
					ajson = json.loads(line)
					for key in ajson:
						print "set "+"CLAVE="+"si_party:"+ajson[key].encode('utf-8') + "  VALOR=" +key.encode('utf-8')
						print "Registros insertados: " + str(redisClient.set("si_party:"+ajson[key].encode('utf-8'),key.encode('utf-8')))
						print
			redis.sendRedis(function)	
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de sinonimos: \n" + str(ex))
def loadSy_Site():
	try:     
		with fm.readFile("cargue_site.txt",fm.path['loads']) as file:
			def function(redisClient):
				for line in file:
					ajson = json.loads(line)
					for key in ajson:
						print "set "+"CLAVE="+"si_site:"+ajson[key].encode('utf-8') + "  VALOR=" +key.encode('utf-8')
						print "Registros insertados: " + str(redisClient.set("si_site:"+ajson[key].encode('utf-8'),key.encode('utf-8')))
						print
			redis.sendRedis(function)	
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de sinonimos: \n" + str(ex))

def loadParty():	
	try:
	    with fm.readFile("partys.json",fm.path['loads']) as partys:
		def function(redisClient):					
			for party in partys:
				jparty = json.loads(party)
				print "set CLAVE= party:" + jparty["Url"].encode('utf-8')+" VALOR= "+jparty["Name"].encode('utf-8')
				print "Registros insertados: " + str(redisClient.set("party:" + jparty["Url"].encode('utf-8'),jparty["Name"].encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo para la carga de partidos: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de los partidos: \n" + str(ex))
def loadAsociation():
	try:     
		entities = fm.readJSONFile("entities.json",fm.path['loads'])
		def function(redisClient):					
			for clase_nodo in entities:
				print "set CLAVE= entity:" + clase_nodo.encode('utf-8')+" VALOR= "+entities[clase_nodo].encode('utf-8')
				print "Registros insertados: " + str(redisClient.set("entity:"+clase_nodo.encode('utf-8'),entities[clase_nodo].encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de las entidades: \n" + str(ex))
def loadSy_Org():
	try:     
		with fm.readFile("cargue_organization.txt",fm.path['loads']) as file:
			def function(redisClient):
				for line in file:
					ajson = json.loads(line)
					for key in ajson:
						print "set "+"CLAVE="+"si_org:"+ajson[key].encode('utf-8') + "  VALOR=" +key.encode('utf-8')
						print "Registros insertados: " + str(redisClient.set("si_org:"+ajson[key].encode('utf-8'),key.encode('utf-8')))
						print
			redis.sendRedis(function)	
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de sinonimos para organizaciones: \n" + str(ex))

def loadSy_inst():
	try:     
		with fm.readFile("cargue_institution.txt",fm.path['loads']) as file:
			def function(redisClient):
				for line in file:
					ajson = json.loads(line)
					for key in ajson:
						print "set "+"CLAVE="+"si_inst:"+ajson[key].encode('utf-8') + "  VALOR=" +key.encode('utf-8')
						print "Registros insertados: " + str(redisClient.set("si_inst:"+ajson[key].encode('utf-8'),key.encode('utf-8')))
						print
			redis.sendRedis(function)	
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de sinonimos para instuciones: \n" + str(ex))

def loadOntology(): 
	try:     
		ontyJSON = fm.readJSONFile("ontology.json",fm.path['loads'])
		def function(redisClient):					
			for clase_nodo in ontyJSON['nodes']:
				for prop in ontyJSON['nodes'][clase_nodo]:
					print "sadd node " + clase_nodo.encode('utf-8')+" -> "+prop.encode('utf-8')
					print "Registros insertados: " + str(redisClient.sadd("node:"+clase_nodo.encode('utf-8'),prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de la ontologia: \n" + str(ex))
def loadStrctureParty():
	try:     
		structureJSON = fm.readJSONFile("partyStrcture.json",fm.path['loads'])
		def function(redisClient):
			for prop in structureJSON:
				print "sadd party_node" +" -> "+prop.encode('utf-8')
				print "Registros insertados: " + str(redisClient.sadd("party_node",prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura de partidos: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de los partidos: \n" + str(ex))
def loadStructureSite():
	try:     
		structureJSON = fm.readJSONFile("siteStructure.json",fm.path['loads'])
		def function(redisClient):
			for prop in structureJSON:
				print "sadd site_node" +" -> "+prop.encode('utf-8')
				print "Registros insertados: " + str(redisClient.sadd("site_node",prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura de sitios: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de los sitios: \n" + str(ex))

def loadStructureOrg():
	try:     
		structureJSON = fm.readJSONFile("organizationStructure.json",fm.path['loads'])
		print structureJSON 
		def function(redisClient):
			for prop in structureJSON:
				print "sadd site_node" +" -> "+prop.encode('utf-8')
				print "Registros insertados: " + str(redisClient.sadd("org_node",prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura organizaciones: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de las organizaciones: \n" + str(ex))

def loadStructureSite():
	try:     
		structureJSON = fm.readJSONFile("siteStructure.json",fm.path['loads'])
		def function(redisClient):
			for prop in structureJSON:
				print "sadd site_node" +" -> "+prop.encode('utf-8')
				print "Registros insertados: " + str(redisClient.sadd("site_node",prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura de sitios: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de los sitios: \n" + str(ex))

def loadStructureInsitution():
	try:     
		structureJSON = fm.readJSONFile("institutionStructure.json",fm.path['loads'])
		def function(redisClient):
			for prop in structureJSON:
				print "sadd inst_node" +" -> "+prop.encode('utf-8')
				print "Registros insertados: " + str(redisClient.sadd("inst_node",prop.encode('utf-8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura de instuciones: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de los instuciones: \n" + str(ex))


def getStructureParty():
	def function(redisClient):
		dic = {}
		for property in redisClient.smembers("party_node"):
			dic[property] = ""
		return dic
	return redis.sendRedis(function)
def getStructureSite():
	def function(redisClient):
		dic = {}
		for property in redisClient.smembers("site_node"):
			dic[property] = ""
		return dic
	return redis.sendRedis(function)

def getStructureInst():
	def function(redisClient):
		dic = {}
		for property in redisClient.smembers("site_node"):
			dic[property] = ""
		return dic
	return redis.sendRedis(function)
def getStructureOrg():
	def function(redisClient):
		dic = {}
		for property in redisClient.smembers("org_node"):
			dic[property] = ""
		return dic
	return redis.sendRedis(function)

def getStructure():
	def function(redisClient):
		dic = {}
		for node in redisClient.keys('node:*'):
			dic[node.replace('node:','')] = {}
		for node in redisClient.keys('node:*'):
			for property in redisClient.smembers(node.encode('utf-8')):
				dic[node.replace('node:','')][property] = []
		return dic
	return redis.sendRedis(function)
def getParty():
	def function(redisClient):
		dic = {}
		for node in redisClient.keys('party:*'):
			dic[node.replace('party:','')] = redisClient.get(node)
		return dic
	return redis.sendRedis(function)
def getEntities():
	def function(redisClient):
		dic = {}
		for node in redisClient.keys('entity*'):
			dic[node.replace('entity:','')]= redisClient.get(node)
		return dic
	return redis.sendRedis(function)	


	

def getSynonyms():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('sinonimo*'):
			dic[synom.replace('sinonimo:','')]=redisClient.get(synom).split(':')
		return dic
	return redis.sendRedis(function)
def getSy_Party():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('si_party*'):
			dic[synom.replace('si_party:','')]=redisClient.get(synom)
		return dic
	return redis.sendRedis(function)
def getSy_Site():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('si_site*'):
			dic[synom.replace('si_site:','')]=redisClient.get(synom)
		return dic
	return redis.sendRedis(function)

def getSy_Org():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('si_org*'):
			dic[synom.replace('si_org:','')]=redisClient.get(synom)
		return dic
	return redis.sendRedis(function)

def getSy_Inst():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('si_inst*'):
			dic[synom.replace('si_inst:','')]=redisClient.get(synom)
		return dic
	return redis.sendRedis(function)
def cleanDataBase():
	def function(redisClient):
		redisClient.flushall()
	redis.sendRedis(function)


def recorrerGranEstructra():
	try:     
		structureJSON = fm.readJSONFile("generalStructure.json",fm.path['loads'])
		def function(redisClient):
			for prop in structureJSON:				
				for item in structureJSON[prop]:
					if isinstance(structureJSON[prop][item] ,dict):
						for key in structureJSON[prop][item]:
							for key_2 in structureJSON[prop][item][key]:
								print "hset noderel_" + prop.encode('utf-8')+"_"+key.encode('utf-8') +" "+key_2+" "+str(structureJSON[prop][item][key][key_2])
								print "Registros insertados: " + str(redisClient.hset("noderel_"+prop.encode('utf-8')+"_"+key.encode('utf-8') ,key_2,str(structureJSON[prop][item][key][key_2])))
					else:					
						print "hset node_" + prop.encode('utf-8') +" "+item.encode('utf-8') +" "+structureJSON[prop][item]
						print "Registros insertados: " + str(redisClient.hset("node_" + prop.encode('utf-8'),item.encode('utf-8'),structureJSON[prop][item].encode('utf8')))
		redis.sendRedis(function)
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo de estructura de instuciones: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la cargar la estructura de los instuciones: \n" + str(ex))	
def getGranEstructura():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('node_*'):
			dic[synom.replace('node_','')]= {'relation':{},'style':redisClient.hgetall(synom)}			
			for synom_2 in redisClient.keys('noderel_'+synom.replace('node_','')+'*'):
				dic[synom.replace('node_','')]['relation'][synom_2.replace('noderel_'+synom.replace('node_','')+'_','')]= redisClient.hgetall(synom_2)			
		return dic
	return redis.sendRedis(function)

def startDatabase():
	cleanDataBase()	
	loadCategories()
	loadSynonyms()
	loadOntology()
	loadAsociation()
	loadParty()
	loadStrctureParty()
	loadSynonyms_party()
	loadStructureSite()
	loadSy_Site()
	loadSy_Org()
	loadStructureOrg()
	loadSy_inst()
	recorrerGranEstructra()
#startDatabase()
#loadStructureInsitution()
#loadSy_inst()
#cleanDataBase()	
#
#getStructure()
#startDatabase()