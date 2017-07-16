import wikipedia
import pyScraper 
import Libraries.pyRedis as redis
# -*- coding: utf-8 -*-
wikipedia.set_lang("es")

categorias = redis.getSet("categoria")

#Returns a wikipedia object
def getPage(search):
    return wikipedia.page(search) 

#Returns a list with the results of a serch
def search(search):
	return wikipedia.search(search)	
	
#Get wikipedia page categories
def getCategories(page):
    return page.categories #Get the categories of a page from Wikipedia


def getSuggestion(search):
	return wikipedia.suggest(search)

#Returns un json with the principal elements of a serch
def getPageData(search):
	dic ={}
	try:
		dic["Title"]=search
		page =  getPage(search)
		dic["Url"]=page.url
		try: 		
			dic["Imagen"]= pyScraper.getTableImage(page.url)
		except Exception as errorImg:
			dic["Imagen"]= "Imagen no disponible"
		print set(getCategories(page))
		dic["Politic"] = bool(set([x.encode("utf-8") for x in getCategories(page)]) & set(categorias))
		return dic
	except Exception as error:
		print str(error)


print(search("https://es.wikipedia.org/wiki/Enrique_Santos_Castillo"))