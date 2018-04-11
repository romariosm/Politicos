import json
from py2neo import Graph, Path, authenticate, Node

#Loads the configuration file
try:
	with open("config.json",'r') as c:#Open the file
		path = json.load(c)
except Exception as error:
	print "The configuration file to NEO4J database no exists" + str(error)

# set up authentication parameters
authenticate(path['databases']['neo4j']['host'] + ":" + str(path['databases']['neo4j']['port']), 
	path['databases']['neo4j']["auth"]["user"], 
	path['databases']['neo4j']["auth"]["psw"])

graph = Graph("http://" +  path['databases']['neo4j']['host'] + ":" + str(path['databases']['neo4j']['port']) + "/db/data/")

def sendToNeo(sentence):
	return graph.run(sentence)#.dump()

