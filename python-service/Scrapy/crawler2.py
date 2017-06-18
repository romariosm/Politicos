import wikipedia 
import pyScraper
import pyWiki
import Libraries.FileManager as fm


wikipedia.set_lang("es")
dic = { }
def obtenerPaginas(persona):
	print "Relaciones Familiares: "
	print
	page = wikipedia.page(persona)
	imprimirLinks(page.url,persona)
	fm.writeFileJSON("test",dic)
	print
	print "Relaciones Laborales: "
	print	
	info = pyScraper.politic_scrapeTable(page.url)
	if info.has_key("laboral - links"):
		for item in info["laboral - links"]:
			for link in item:
				if "Archivo" not in link["url"]:
					print link["title"].encode("utf-8") + ": "+ link["url"].encode("utf-8")
		 

visitadas = set()

def imprimirLinks(url,persona):	
	info = pyScraper.politic_scrapeTable(url)
	dic[persona.encode("utf-8")] = {}
	if info.has_key("Familia"):
		for item in info["Familia"]:
			if "links" in item:
				for link in info["Familia"][item]:
					if item.strip(" - links").encode("utf-8")+ link["url"].encode("utf-8") not in visitadas:
						if "#cite" not in link["url"]:
							relacion =  item.strip(" - links").encode("utf-8")
							if dic[persona.encode("utf-8")].has_key(relacion):
								dic[persona.encode("utf-8")][relacion].append(link["url"].encode("utf-8"))
							else:
								dic[persona.encode("utf-8")][relacion] = [link["url"].encode("utf-8")]
							#print persona.encode("utf-8")+" "+ item.strip(" - links").encode("utf-8")+" "+link["title"].encode("utf-8")+" "+link["url"].encode("utf-8")
							visitadas.add(item.strip(" - links").encode("utf-8")+ link["url"].encode("utf-8"))
							imprimirLinks(link["url"] ,link["title"])


obtenerPaginas("Juan Manuel Santos Calderon")