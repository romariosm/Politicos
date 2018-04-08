import json
import time
import pyScraper
import estructurador
import sys

reload(sys)
sys.setdefaultencoding('utf8')
letra = u'[{"url": "https://es.wikipedia.org/wiki/H%C3%A9ctor_Abad_G%C3%B3mez", "ns": 0, "pageid": 627112, "title": "H\xe9ctor Abad G\xf3mez"}, {"url": "https://es.wikipedia.org/wiki/Miguel_Abad%C3%ADa_M%C3%A9ndez", "ns": 0, "pageid": 104318, "title": "Miguel Abad\xeda M\xe9ndez"}, {"url": "https://es.wikipedia.org/wiki/Gabriel_Acosta_Bendek", "ns": 0, "pageid": 1242069, "title": "GaH\xe9briel Acosta Bendek"}]'

#Loads the configuration file
try:
	with open("URLPoliticos.txt","r") as c:#Open the file
		#texto = c.read().replace("'",'"').replace(': u"',': "').replace(', u"',', "').replace("\\",'')
		i = 0
		path = c.readlines()
		with open("Generated Files/infoPersonal.txt",'a') as g:#Open the file
			for item in path:
				try:
					print
					print i
					linea = ""
					estructurador.createTree(item,[],[])
					#politic = pyScraper.politic_scrapeTable(item)
					#a = estructurador.create_structure(politic)
					#c = estructurador.cleanStructure(a)
					i += 1
					"""for info in c['person']:
						linea +=  "|"  + c['person'][info]
					g.write(linea.encode("utf8").replace("\n","").replace("\r","") + "\n")"""
					if i == 30:
						break
				except Exception as subEx:
					print (item) + ":	" + str(subEx)
					pass
except Exception as error:
	print "Error: " + str(error)
