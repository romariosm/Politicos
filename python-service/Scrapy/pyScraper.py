#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import time
import Libraries.FileManager as fm
import Libraries.JSONProcessor as jsonp
import json
# -*- coding: utf-8 -*-

#Returns a Beutiful object
def getSoup(url):
	response = urllib2.urlopen(url) #Load the URL
	return BeautifulSoup(response.read(),"html.parser")  #Load the structure html to the library     

#Get the title of the page
def getTitle(soup):
	return soup.title.string

#Returns a element with infobox table
def getTable(soup): 
	return soup.find('table', 'infobox')

#Scrapy of the imge in the infobix table
def getTableImage(url):
	try:
		return "https:" + getTable(getSoup(url)).find_all('tr')[1].find_all('img')[0]['src']
	except Exception as error:
		return "no disponible"
		
#Scrapy infobox (Proven for politicians) into json structure
def politic_scrapeTable(url):
	soup = getSoup(url)
	table = soup.find('table', 'infobox')
	table = getTable(soup)
	dic={}
	try:
		if soup is not None:
			dic = jsonp.addValue(dic,"Fecha de registro", time.strftime("%x") + " " + time.strftime("%X"))
			dic = jsonp.addValue(dic,"Nombre",getTitle(soup).replace(' - Wikipedia, la enciclopedia libre',''))
			dic = jsonp.addValue(dic,"Url",url)
			dic = jsonp.addValue(dic,"Imagen",getTableImage(url))			
			filas = table.find_all('tr')[2:]
			dic["laboral - links"] = []
			parent = ""
			for fil in filas:
				if len(fil.find_all('th'))>0 and len(fil.find_all('td'))<1:
					parent = jsonp.eliminateCharacters(jsonp.clearValue(fil.find_all('th')[0].text))
					dic["laboral - links"].append(getLinks(fil.find_all('th')[0]))
					dic = jsonp.addValue(dic,parent,{})
				elif len(fil.find_all('th')) > 0  and len(fil.find_all('td')) > 0:
					if parent != "":
						
						data_clean=jsonp.clearValue(''.join(value for value in fil.find_all(text=True) if value.parent.name != 'a' and value.parent.name != 'th' and value != '' and value != ' ' and value != '\n' ))
						#print data_clean, "--------"
						if hasattr(data_clean, '__iter__'):
							if len(data_clean)>0:
								dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, [{'title': text, 'url': None } for text in data_clean if text != '' and text != ''])
						elif data_clean != '':
							dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, [{'title': data_clean, 'url': None }])
						 
						if len(fil.find_all('td')[0].findAll('a'))>0:
							
							if dic[parent].has_key(jsonp.eliminateCharacters(fil.find_all('th')[0].text)):

								for link in getLinks(fil.find_all('td')[0]):
									print link.get('url')
									if link.get('url'):
										dic[parent][fil.find_all('th')[0].text].append(link)																
							else:
								dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, getLinks(fil.find_all('td')[0]))
					else:
						dic = jsonp.addValue(dic,fil.find_all('th')[0].text, fil.find_all('td')[0].text)		
	except Exception as error:
	   	fm.registerError(str(error))
	return dic 

#fm.writeFileJSON("prueba",politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos"))


def getLinks(element):
	temp = []
	for link in element.findAll('a'):
		if "wikidata" not in link.get('href'):
			enlace = {}
			#print link
			#print link.text
			enlace["title"] = link.get('title')
			#enlace["text"] =link.text
			if "http" in link.get('href'):
				enlace["url"] = link.get('href')
			else:
				enlace["url"] ="https://es.wikipedia.org" + link.get('href')
			temp.append(enlace)
	return temp

#fm.writeFileJSON('test_enri',politic_scrapeTable("https://es.wikipedia.org/wiki/Enrique_Santos_Castillo"))


#parsed = json.loads()
#print json.dumps(politic_scrapeTable("https://es.wikipedia.org/wiki/Juan_Manuel_Santos"), indent=4, sort_keys=True)
print json.dumps(politic_scrapeTable("https://es.wikipedia.org/wiki/%C3%81lvaro_Uribe"), indent=4, sort_keys=True)
