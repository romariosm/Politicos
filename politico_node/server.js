var express=require('express') //Import 
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front 
var MongoClient = require('mongodb').MongoClient, 
					assert = require('assert'); //May be es errores
var properties = require('./properties.json')
var redis = require('redis')
var mongo = require('mongodb');
var structurer = require('./structurer.js');

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //REderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML 
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)



function testRedis(redisClient){
	//redisClient.set('test','It's working,redis.print)
	redisClient.get('test',function(error,value){
			if(error){
				throw error
			}
			console.log("Testing a query in redis")
			console.log("-->" + value)
		})
}

function getSetRedis(redisClient,query,callback){
	redisClient.smembers(query, function(err,result){
		callback(result)
	})
}


var options = { root: __dirname + '/static/'}

app.get('/', function(request, response){ //Start the main page 
	console.log("Conecting to Node Server...")
	response.render('index.html');
	console.log("Connection completed");
	structurer.getEstructure(function(estructura){console.log(estructura)})
	//sendNeo4j()
	//sendRedis(testRedis);
	//sendRedis(function(redisClient){
	//	getSetRedis(redisClient,"nodos:Lugar", function(result){console.log(result)})
	//})
}).listen(properties.node.port) 

function sendMongo(callback){
	var url = 'mongodb://' + properties.mongo.host+':'+properties.mongo.port+'/'+properties.mongo.database;
	MongoClient.connect(url, function(err, db) {
		if (err){
			console.log("Se presentó error" + err)
		}
		assert.equal(null, err);		
		callback(db);
		db.close();
	});

}
function sendRedis(callback){	
	var redisClient = redis.createClient(properties.redis.port, properties.redis.host)
	redisClient.on('error',function(error){
		console.log("Se presentó un error con redis")
	})
	callback(redisClient)
	redisClient.quit();
}

app.use(express.static('static')); 

app.get('/send_political', function(request, response){

	
});

app.get('/search/person:*', function(request, response){

	var political=request.query.search

	context = {}
	list_political=[]
	quantity_characters=9
	initial=0
	page=1
	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"Nombre": {"$in": [new RegExp(political, "i") ]} }).toArray(function(err, result) {
	 		//console.log(result)

	 		num_pages=Math.ceil(result.length/quantity_characters)

	 		if(request.query.page){

	 			if(request.query.page<1){
					page=1
					initial=quantity_characters*(parseInt(page)-1)

				}else if(request.query.page>num_pages){
					page=num_pages
					initial=quantity_characters*(parseInt(page)-1)
				}else{
					page=request.query.page
					initial=quantity_characters*(parseInt(page)-1)
				}

			}else{

				initial=0
			}


	 		if (result.length>(quantity_characters*page)){
	 			len=quantity_characters*page
	 		}else{
	 			len=result.length
	 		}

	 
	 		
    		for(var i=initial;i<len;i++){

    			dict_personaje={}

    			dict_personaje['id']=result[i]._id

    			if(result[i].Nombre){

    				dict_personaje['nombre']=result[i].Nombre
    			}else{
    				dict_personaje['nombre']=''
    			}

    			if(result[i].Imagen != 'No_Disponible' ){
    				dict_personaje['foto']=result[i].Imagen

    			}else{
    				dict_personaje['foto']='/images/hombre.png'
    			}

    			if (result[i]['Información personal']){
	    			if(result[i]['Información personal']['Nacionalidad']){
	    				dict_personaje['nacionalidad']=result[i]['Información personal']['Nacionalidad']

	    			}else{
	    				dict_personaje['nacionalidad']=''
	    			}
	    			if(result[i]['Información personal']['Nacimiento']){
	    				dict_personaje['nacimiento']=result[i]['Información personal']['Nacimiento'][0]

	    			}else{
	    				dict_personaje['nacimiento']=''
	    			}

	    			if(result[i]['Información personal']['Residencia']){
	    				dict_personaje['residencia']=result[i]['Información personal']['Residencia']

	    			}else{
	    				dict_personaje['residencia']=''
	    			}
    			}else{
    				dict_personaje['nacionalidad']=''
    				dict_personaje['nacimiento']=''
    				dict_personaje['residencia']=''
    			}
   	
    			
				if(result[i]['Información profesional']){
					if(result[i]['Información profesional']['Ocupación']){
	    				dict_personaje['ocupacion']=result[i]['Información profesional']['Ocupación']
	    			}else{
	    				dict_personaje['ocupacion']=''
	    			}
				}else{
					dict_personaje['ocupacion']=''
				}	

    			

				list_political.push(dict_personaje)
			}
			context['political_list']=list_political
			context['search']=request.query.search
			context['num_pages']=num_pages
			context['current_page']=page
			response.render('search_political.html',context)

			

			
 		});
	})

    });

app.get('/search/getsuggestion', function(request, response){

	socket.emit('search suggestions', request.query.search)

	socket.on('suggestion response', function(msg) {

		data={}
		data['suggestions']=msg
		response.end(JSON.stringify(data))

	})
	




	
})




app.get("/autocomplete/politicos", function (request,response) {
	var nombre=request.query.query
	var arreglo=[]

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"Nombre": {"$in": [new RegExp(nombre, "i") ]} }).toArray(function(err, result) {
	 		console.log({"Nombre": {"$in": [/nombre/i] } })
    		for(var i=0;i<result.length;i++){
				arreglo.push({'data':String(result[i]._id),'value':result[i].Nombre})
			}
			response.end(
				JSON.stringify({"query": request.query.query,"suggestions": arreglo})
			)
 		});
	})
})

app.get('/load/person:*', function(request, response){


	console.log(request.query.id)
	var political_id = new mongo.ObjectID(request.query.id);
	context={}

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"_id": political_id }).toArray(function(err, result) {
	 		console.log(result)
    		
		info={}

		info['nombre']=result[0].Nombre
		info['imagen']=result[0].Foto

		if(result[0]['Información personal']['Residencia']){
			info['residencia']=result[0]['Información personal']['Residencia']

		}else{
			info['residencia']=''
		}

		if(result[0]['Información profesional']){
					if(result[0]['Información profesional']['Ocupación']){
	    				info['ocupacion']=result[0]['Información profesional']['Ocupación']
	    			}else{
	    				info['ocupacion']=''
	    			}
				}else{
					info['ocupacion']=''
				}

		context['info']=info
		structurer.getEstructure(function(estructura){
			list_nodes=[]
			list_links=[]
			estructura.forEach(function(element){
				console.log(element)

				for(node in element){

					if(list_nodes.findIndex(i => i.id == element[node]._id) == -1 && node != 'r'){
						console.log(node)

						node_p={}
						node_p.id=element[node]._id
						node_p.name=element[node].properties.name
						node_p.residency=element[node].properties.residency
						node_p.nacionality=element[node].properties.religion
						node_p.url=element[node].properties.Url
						node_p.group=1
						//console.log(node_p)

						list_nodes.push(node_p)

					}else if (list_links.findIndex(i => i.id == element[node]._id)== -1 && node == 'r'){
						link={}
						link.id=element[node]._id
						link.type=element[node].type
						link.source=element[node]._fromId
						link.target=element[node]._toId

						list_links.push(link)

					}
				}

			})

			graph={}
			graph.nodes=list_nodes
			graph.links=list_links

			context.graph=JSON.stringify(graph)
			response.render('graph_political.html',context)
			
		})	

		
 		});
	})


	


})

app.get('/search/getDataSuggestion', function(request, response){		
	socket.emit('search dataSuggestions', request.query.search)

	socket.on('suggestion dataResponse', function(data) {


		sendMongo(function (db){

			if(data != null){

				db.collection(properties.mongo.collections).find({"Url":  data.Url }).toArray(function(err, result) {

			 		//console.log({"Nombre": {"$in": [/nombre/i] } })
		    		if(result.length>0){
		    			
		    			
		    			response.end(JSON.stringify(null))
		    			
		    			
		    		}else{

		    			response.end(JSON.stringify(data))

		    		}
		    		

	 			});

	 		}else{
	 			response.end(JSON.stringify(data))
	 		}	 	
		})


	
	
})

})


app.get('/search/getScrapy', function(request, response){ 

	context = {}
	socket.emit('search politician', request.query.url)
	socket.on('my response', function(msg) {    	
    	person = {}
    	socket.emit('create create_structure', msg)
		socket.on('get structure', function(structure) {
			structurer.createPerson(structure.person);
			console.log(structure)
			structurer.createParty(structure.party);    	
			structurer.createRelation(structure.person,structure.party,'pertenece')

			
    	})
    	/*sendMongo(function(database){
    		database.collection(properties.mongo.collections).insertMany([msg])
    		response.end(msg.Nombre)

    		
    		}
    	);
		console.log(msg)*/

	});
})       

