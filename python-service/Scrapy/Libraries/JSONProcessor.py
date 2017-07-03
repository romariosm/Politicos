import json
# -*- coding: utf-8 -*-
        
#Returns a array or a string without empty values 
def clearValue(sentence):
    temp = sentence.split("\n")
    if len(temp)==1:
        return temp[0]
    else:
        if "" in temp:
            return clearValue(''.join(filter(lambda a: a != "", temp)))
        else:
            return temp

#Eliminates characters that generate conflicts with json structure
def eliminateCharacters(cadena):
    d={'[':'',']':'','.':'',';':'',u'\u00ba':'','1':'','2':'','3':'','4':'','5':'','6':'','7':'','8':'','9':'','0':''}
    return (''.join(d[s] if s in d else s for s in cadena)).strip()

#Eliminates characters that generate conflicts with json structure
def eliminateCharacters_title(cadena):
    d={'[':'',']':'','.':'',';':'',u'\u00ba':''}
    return (''.join(d[s] if s in d else s for s in cadena)).strip()

#Adds Values to a dictionary
def addValue(dictionary,name,value):
    name = eliminateCharacters(name)
    dictionary[name]=value
    return dictionary #Return the dictionary with a new value