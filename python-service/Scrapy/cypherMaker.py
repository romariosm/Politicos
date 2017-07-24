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

def makeRelation(label,properties, labelA,nodoA,labelI,nodoI):
	return len(list(sendToNeo("MATCH (a:"+labelA+" "+makeJsonNeo(nodoA)+"), (i:"+labelI+" "+makeJsonNeo(nodoI)+") CREATE (a)-[r:"+label+" "+makeJsonNeo(properties)+"]->(i) return r"))) != 0

def existsRelation(label,properties, labelA,nodoA,labelI,nodoI):
	return len(list(sendToNeo("MATCH (a:"+labelA+" "+makeJsonNeo(nodoA)+")-[r:"+label+" "+makeJsonNeo(properties)+"]->(i:"+labelI+" "+makeJsonNeo(nodoI)+") return r"))) != 0

def getPersonalFamiliarInfo(properties,level):
	return list(sendToNeo("MATCH (p "+ makeJsonNeo(properties) +")-[q*1.."+level+"]->(r) return p,q,r"))
