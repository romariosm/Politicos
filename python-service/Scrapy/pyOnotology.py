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

def getStructure():
	def function(redisClient):
		dic = {}
		for node in redisClient.keys('node*'):
			dic[node.replace('node:','')] = {}
		for node in redisClient.keys('node*'):
			for property in redisClient.smembers(node.encode('utf-8')):
				dic[node.replace('node:','')][property] = []
		return dic
	return redis.sendRedis(function)
def getSynonyms():
	def function(redisClient):
		dic = {}
		for synom in redisClient.keys('sinonimo*'):
			dic[synom.replace('sinonimo:','')]=redisClient.get(synom).split(':')
		return dic
	return redis.sendRedis(function)

def cleanDataBase():
	def function(redisClient):
		redisClient.flushall()
	redis.sendRedis(function)

def startDatabase():
	cleanDataBase()	
	loadCategories()
	loadSynonyms()
	loadOntology()
	
#startDatabase()
#print getStructure()
#print getSynonyms()