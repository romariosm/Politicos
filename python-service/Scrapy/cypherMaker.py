from neo4j import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# -*- coding: utf-8 -*-
def exists(label,properties):
	return len(list(sendToNeo("MATCH (p:"+label+" "+makeJsonNeo(properties)+") return p"))) != 0

def create(label,properties):
	return len(list(sendToNeo("CREATE (p:"+label+" "+makeJsonNeo(properties)+") return p"))) != 0

def makeJsonNeo(properties):	
	return u"{"+",".join([key + ":'" +properties[key]+"'" for key in properties]).encode('utf-8').strip()+u"}"

def makeRelation(label,labelA,nodoA,labelI,nodoI):
	print"MATCH (a:"+labelA+" "+makeJsonNeo(nodoA)+"), (i:"+labelI+" "+makeJsonNeo(nodoI)+") CREATE (a)-[r:"+label+"]->(i) return r"
	return len(list(sendToNeo("MATCH (a:"+labelA+" "+makeJsonNeo(nodoA)+"), (i:"+labelI+" "+makeJsonNeo(nodoI)+") CREATE (a)-[r:"+label+"]->(i) return r"))) != 0

