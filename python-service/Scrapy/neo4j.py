import json
from py2neo import Graph, Path, authenticate, Node

# set up authentication parameters
authenticate("localhost:7474", "neo4j", "1234")
graph = Graph("http://localhost:7474/db/data/")

def sendToNeo(sentence):
	return graph.run(sentence)#.dump()

