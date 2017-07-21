from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import pyWiki
from pyScraper import *
import Libraries.FileManager as fm
from estructurador import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#@app.route('/')
#def index():
#    return render_template('index.html')

@socketio.on('search politician', namespace='/')
def test_message(message):
	try:
		emit('my response', politic_scrapeTable(message))
	except Exception as  e:
		fm.registerError("Error en el scraper del personaje: " + str(error))
	else:
		pass
	finally:
		pass
	

@socketio.on('search suggestions', namespace='/')
def getSuggestion(message):
	print "La busqueda es: "
	print message
	emit('suggestion response', pyWiki.search(message))

@socketio.on('search dataSuggestions', namespace='/')
def getDataSuggestion(message):
	print message
	emit('suggestion dataResponse', pyWiki.getPageData(message))



@socketio.on('create create_structure', namespace='/')
def getStructure(message):
	emit('get structure', cleanStructure(create_structure(message)))

@socketio.on('create savePerson', namespace='/')
def createPerson(message):	
	emit('create person', savePerson(message))

@socketio.on('relate relatedFamily', namespace='/')
def relateFamily(message):	
	emit('create family', relatedFamily(message))


@socketio.on('relate relateOrganizations', namespace='/')
def relate_Organizations(message):	
	emit('create organization', relateOrganizations(message,'party') + relateOrganizations(message,'laboral') + relateOrganizations(message,'academic'))

#@socketio.on('connect', namespace='/')
#def test_connect():
#    emit('my response', {'data': 'Connected'})

#@socketio.on('disconnect', namespace='/')
#def test_disconnect():
#    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)

    