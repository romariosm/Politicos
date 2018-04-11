# -*- coding: utf-8 -*-
import json
import redis

#Loads the configuration file
try:
	with open("config.json",'r') as c:#Open the file
		path = json.load(c)
except Exception as error:
	print "The configuration file no exists" + str(error)

def sendRedis(callback):
	redisClient = redis.StrictRedis(host=path['databases']['redis']['host'], port=path['databases']['redis']['port'], db=path['databases']['redis']['db']) 
	return callback(redisClient)

def testRedis(redisClient):
	print(redisClient.get('test'))

def addSet(root, json):
	for subRoot in json:
		clave = root + ':' + subRoot
		for i in range(0,len(json[subRoot])):
			print("sadd "+clave.encode("utf-8")+" " +json[subRoot][i].encode("utf-8"))
			def function(redisClient):
				return "Registros insertados: " + str(redisClient.sadd(clave,json[subRoot][i]))
			print(self.sendRedis(function))

def getSet(query):
	def function(redisClient):
				return redisClient.smembers(query)
	return sendRedis(function)

sendRedis(testRedis)
