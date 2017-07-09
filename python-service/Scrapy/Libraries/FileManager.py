# -*- coding: utf-8 -*-
import json 
import time

#Loads the configuration file 
try:      
	with open("config.json",'r') as c:#Open the file 
		path = json.load(c)
except Exception as error:
	print "The configuration file no exists" + str(error)
	
#Writes at the log file the generated errors
def registerError(message):
	try:      
		with open(path[u"generatedFilePath"] + path[u"logFile"],'a') as g:#Open the file 
			g.write("--------------------------------------------------------\n")
			g.write(time.strftime("%x") + " " + time.strftime("%X") + "\n")
			g.write(message)
			g.write("\n")
	except IOError as error:
		open(path[u"generatedFilePath"] + path[u"logFile"],'w')
		registerError(message)
	except Exception as error:
		print "Error not registered \n" + message

#Writes json files 
def writeFileJSON(file, line):
	try:      
		with open(path["generatedFilePath"] + file + ".json",'a') as g:#Open the file 
			json.dump(line, g) 
			g.write("\n")
	except IOError:
		open(path["generatedFilePath"] + file + ".json",'w')
		writeFileJSON(path["generatedFilePath"] + file + ".json", line)
	except Exception as error:
		registerError("Error: " + error)

#Return the file lines
def readFile(file, dir = path["filePath"]):
	try:      
		print dir + "/" + file
		return open(dir + "/" + file,'r')
	except IOError:
		registerError("No se puede leer el archivo: " + file)
