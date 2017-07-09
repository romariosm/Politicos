var express=require('express') //Import 
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front 
var MongoClient = require('mongodb').MongoClient, 
					assert = require('assert'); //May be es errores
var properties = require('./properties.json')
var redis = require('redis')
var mongo = require('mongodb');
var neo4j = require('neo4j');

app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //Renderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML 
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)

app.get('/', function(request, response){ //Start the main page 
	console.log("Conecting to Node Server...")
	console.log("Connection completed");
}).listen(properties.node.port+1)  //Mientras :3


function iniciar(inicio){ 
	context = {}
	socket.emit('search politician', inicio)
	socket.on('my response', function(msg) {
    	console.log("La Familia es : ")
    	for (property in msg.Familia){
    		if (property.indexOf("links") !=-1){
    			msg.Familia[property].forEach(function(enlace){  
    				console.log(msg.Nombre +" ->  "+property.replace("- links","") + "  " +enlace.title + " " + enlace.url);
    				//pseudoCrawler(enlace.url)
    			})
    		}     		
    	}
    	console.log("Los trabajos son: ")
    	msg['laboral - links'].forEach(function(enlaces){
				enlaces.forEach(function(enlace){
					if (enlace.url.indexOf("Archivo")==-1){
						console.log(msg.Nombre + " ->  " + enlace.title + " " + enlace.url);
					}
				})
    		})

	});
})
