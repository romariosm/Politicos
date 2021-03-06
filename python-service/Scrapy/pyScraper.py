#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib
import urllib2
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
	parent = 'default'
	dic = jsonp.addValue(dic,'default',{})
	try:
		if soup is not None:
			dic = jsonp.addValue(dic,"Fecha de registro", time.strftime("%x") + " " + time.strftime("%X"))
			dic = jsonp.addValue(dic,"Nombre",getTitle(soup).replace(' - Wikipedia, la enciclopedia libre',''))
			dic = jsonp.addValue(dic,"Url",url.strip())
			dic = jsonp.addValue(dic,"Imagen",getTableImage(url))
			cargo = None
			if table is not None:
				filas = table.find_all('tr')[1:] if dic['Imagen'] == "No disponible" else table.find_all('tr')[1:]
				for fil in filas:
					if len(fil.find_all('th'))>0:
						if len(fil.find_all('td')) == 0:
							parent = jsonp.eliminateCharacters(jsonp.clearValue(fil.find_all('th')[0].text))
							parent = jsonp.eliminateCharacters(parent)
							dic = jsonp.addValue(dic,parent,{})
							cargo = fil.find_all('th')[0]
						else:
							if parent != "":
								data_clean=jsonp.clearValue(''.join(value for value in fil.find_all(text=True) if value.parent.name != 'a' and value.parent.name != 'th' and value != '' and value != ' ' and value != '\n' ))
								if hasattr(data_clean, '__iter__')and len(data_clean)>0:
									dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, [{'title': jsonp.eliminateCharacters_title(text), 'url': None } for text in data_clean if text != '' and text != ''])
								elif data_clean != '':
									dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, [{'title': jsonp.eliminateCharacters_title(data_clean), 'url': None }])
								if len(fil.find_all('td')[0].findAll('a'))>0:
									if dic[parent].has_key(jsonp.eliminateCharacters(fil.find_all('th')[0].text)):
										for link in getLinks(fil.find_all('td')[0]):
											if link.get('url'):
												dic[parent][jsonp.eliminateCharacters(fil.find_all('th')[0].text)].append(link)
									else:
										dic[parent]=jsonp.addValue(dic[parent], fil.find_all('th')[0].text, getLinks(fil.find_all('td')[0]))
							else:
								"""if len(fil.find_all('td')[0].findAll('a'))>0:
									dic = jsonp.addValue(dic,fil.find_all('th')[0].text, getLinks(fil.find_all('td')[0]))
								else:"""
								dic = jsonp.addValue(dic,fil.find_all('th')[0].text, fil.find_all('td')[0].text)
					else:
						if len(fil.find_all('td')) > 0 and fil.find_all('td')[0].text.strip() != "" and parent != "" and "Wikidata" not in fil.find_all('td')[0].text:
								dic[parent] = jsonp.addValue(dic[parent], 'Perido del cargo', fil.find_all('td')[0].text)
								if cargo != None:
									dic[parent] = jsonp.addValue(dic[parent], 'Entidad', getLinks(cargo))
	except Exception as error:
		print str(eror)
		fm.registerError(url +"\n"+str(error))
	return dic


#Get titles and URL of a structure
def getLinks(element):
	temp = []
	for link in element.findAll('a'):
		if "wikidata" not in link.get('href') and "#cite_note" not in link.get('href') and "Archivo" not in link.get('href') :
			enlace = {}
			enlace["title"] = link.get('title')
			enlace["url"] = link.get('href') if "http" in link.get('href') else "https://es.wikipedia.org" + link.get('href')
			temp.append(enlace)
	return temp

#Get all informaction fro a page
def getContent(url):
	search=url.split('https://es.wikipedia.org/wiki/')[1] if len(url.split('https://es.wikipedia.org/wiki/'))>1 else None
	if search != None:
		page=urllib2.urlopen('https://es.wikipedia.org/w/api.php?action=query&prop=extracts&titles='+search+'&utf8=1&format=json&exlimit=1&explaintext')
		info=json.loads(page.read())
		for key,val in info.get('query').get('pages').items():
			for key1,val1 in info.get('query').get('pages').get(key).items():
				if key1 == 'extract':
					data =val1
	return data

#print politic_scrapeTable("https://es.wikipedia.org/wiki/Santa_Rosa_de_Cabal")
#print politic_scrapeTable("https://es.wikipedia.org/wiki/Germ%C3%A1n_Vargas_Lleras")
#fm.writeFileJSON("juan_santos_prueba",politic_scrapeTable("https://es.wikipedia.org/wiki/Germ%C3%A1n_Vargas_Lleras"))
