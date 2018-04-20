var express=require('express') //Import
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front
var MongoClient = require('mongodb').MongoClient,
					assert = require('assert'); //May be es errores
var properties = require('./properties.json')
var mongo = require('mongodb');
var structurer = require('./structurer.js');
var nodemailer = require('nodemailer');
var redis = require('./pruebaRedis.js');
var neo4j = require('./neo4J.js');
var url_root = '/umaUD'
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //REderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)


app.get('/', function(request, response){ //Start the main page
	console.log("Conecting to Node Server...")
	response.render('index.html');
	console.log("Connection completed");
}).listen(properties.node.port)

function sendMongo(callback){
	var url = 'mongodb://' + properties.mongo.host+':'+properties.mongo.port+'/'+properties.mongo.database;
	MongoClient.connect(url, function(err, db) {
		if (err){
			console.log("Se presentó error" + err)
		}
		assert.equal(null, err);
		callback(db);
		//db.close();
	});

}

app.get('/send_political', function(request, response){


});

app.get('/search/person:*', function(request, response){

	var political=request.query.search

	context = {}
	list_political=[]
	quantity_characters=9
	initial=0
	page=1
	if(political.trim() == ""){
		var query = {}
	}else{
		var query = {"Nombre": new RegExp(political, "i")  }
		
	}
	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find(query).toArray(function(err, result) {
	 		//console.log(result)
			db.close();
                        console.log(err)
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

    			if(result[i].Imagen != 'no disponible' ){
    				dict_personaje['foto']=result[i].Imagen

    			}else{
    				dict_personaje['foto']='/images/hombre.png'
    			}

    			if(result[i].Url){
    				dict_personaje['Url']=result[i].Url
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
	if(request.query.search.trim() != '' && request.query.search.trim() != undefined){
		socket.emit('search suggestions', request.query.search)

		socket.on('suggestion response', function(msg) {

			data={}
			data['suggestions']=msg
			response.end(JSON.stringify(data))
		})
	}else{
		response.end(JSON.stringify({suggestions:[]}))
	}
	
})


app.get("/autocomplete/politicos", function (request,response) {
	var nombre=request.query.query
	var arreglo=[]

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"Nombre": {"$in": [new RegExp(nombre, "i") ]} }).toArray(function(err, result) {
	 		for(var i=0;i<result.length;i++){
				arreglo.push({'data':String(result[i]._id),'value':result[i].Nombre})
			}
			response.end(
				JSON.stringify({"query": request.query.query,"suggestions": arreglo})
			)
 		});
	})
})

function hexToRgbA(hex){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',1)';
    }
    throw new Error('Bad Hex');
}

app.get('/load/person:*', function(request, response){


	var political_id = new mongo.ObjectID(request.query.id);
	context={}

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"_id": political_id }).toArray(function(err, result) {
	 	info={}
		info['nombre']=result[0].Nombre
		console.log('no disponible')
		if(result[0].Imagen == "no disponible"){
			info['imagen']='/images/hombre.png'
		}else{
			info['imagen']=result[0].Imagen
			
		}
		
		var url=result[0].Url
		context['info']=info
		var estructura;
		var sender = function(cadena){
			redis.sendtoPython(
			function(result){
				list_nodes=[]
				list_links=[]
				cadena.forEach(function(element){
					for(node in element){


						if(list_nodes.findIndex(i => i.id == element[node]._id) == -1 && node.indexOf('r') == -1 ){
							
							node_p={}
							node_p.id=element[node]._id
							node_p.labels=element[node].labels[0]

							if(element[node].properties != undefined){
								node_p.url=element[node].properties.Url
								node_p.name=element[node].properties.name
								node_p.info='<div class="col-md-12 dont-break-out"><ul class="list-group">'
								for(subprop in element[node].properties){
									if(checkImageURL(element[node].properties[subprop])){
										node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+' <i class="fa fa-arrow-right" aria-hidden="true"></i>\
										            </strong><img style="object-fit: cover" class="avatar2" height = "70px" width="70px" src="'+element[node].properties[subprop]+'"></div></li>'
									}
									else if(ValidURL(element[node].properties[subprop])){
										node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+': </strong><a href="'+element[node].properties[subprop]+'" >'+element[node].properties[subprop]+'</a></div></li>'
									}
									else{
										if (element[node].properties[subprop].trim() != ""){
											node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+': </strong>'+element[node].properties[subprop]+'</div></li>'
										}
									}
								}
								node_p.info+='</ul></div>'
								if (result[element[node].labels]!= undefined){
									node_p.group=hexToRgbA(result[element[node].labels[0]].style.color)
								}
							}	
							
							list_nodes.push(node_p)
						}else if (list_links.findIndex(i => i.id == element[node]._id) == -1 && node.indexOf('r') != -1 && element[node].length>0){
							if(element[node][0]._id != undefined){
								element[node].forEach( function(element_r, index) {
									if(list_links.findIndex(i => i.id == element_r._id) == -1){
										link={}
										link.id=element_r._id
										link.type=element_r.type
										link.source=element_r._fromId
										link.target=element_r._toId
										link.info='<div class="col-md-12 dont-break-out"><ul class="list-group">'
										for(subprop in element_r.properties){
											link.info=link.info+'\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+ subprop.toUpperCase()+ '</strong>: '+element_r.properties[subprop].replace('5000000',' - ')+'</div></li>'							}
										link.info+='</ul></div>'
										list_links.push(link)

									}
										// statements
								});
							}


						}
					}

				})

				graph={}
				graph.nodes=list_nodes
				graph.links=list_links
				context.graph=JSON.stringify(graph)
				context.nodes=JSON.stringify(result)
				context.url=url
				response.render('graph_political.html',context)
			},'get getNode','getInfo nodeInfo')
		}
		redis.sendtoPython(
					function(result){
						var nodos = result
						var level = 1
						var query = []
						for(key in nodos){
							for(subkey in nodos[key]['relation']){
								var subquery = nodos[key]['relation'][subkey].query.replace('?Url','"'+url+'"')
								if (nodos[key]['relation'][subkey].scrolleable == 1){
									query.push(subquery.replace('?scrolleable',level))
								}
								else{
									query.push(subquery)
								}
							}
						}
						neo4j.sendNeo4j(query.join(' UNION ALL '),sender)

						/*
						Para Romario:
						Quéme la consulta aqui para mostrarle el ejemplo y mostrarle que el mismo còdigo funciona para ambos
						casos para que no quede tan paila la consulta desde aquí toda adicionar una condiciòn para que no traiga
						los sitios en que naciò la persona, pero ps lo importante es por lo menos tener este grafo
						*/
						/*var query = "match (a:person {Url:'https://es.wikipedia.org/wiki/Germ%C3%A1n_Vargas_Lleras'})-[r*1..1]-(i)-[r2*1..1]-(n1)-[r3*1..1]-(n2)-[r4*1..1]-(n3:person {Url:'https://es.wikipedia.org/wiki/Francisco_Santos_Calder%C3%B3n'}) return a,r,i,n1,r2,n2,r3,n3,r4"
						neo4j.sendNeo4j(query,sender)*/
				},'get getNode','getInfo nodeInfo')
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
			socket.emit('create savePerson',structure)
			socket.on('create person', function(politicCreated) {
			})
			socket.emit('relate relatedFamily',structure)
			socket.on('create family', function(familyCreated) {
				sendMongo(function(database){
					familyCreated.forEach(function(element, index){
						database.collection(properties.mongo.collections).find({Url: element.Url}).toArray(function(err, result) {
							if(result.length == 0){
								database.collection(properties.mongo.collections).insertMany(familyCreated)
							}
						})
					})
					database.close()
    				}
    			);

			})
			socket.emit('relate relateOrganizations',structure)
			socket.on('create organization', function(organizationCreated) {
			})
    	})
    	sendMongo(function(database){
    		database.collection(properties.mongo.collections).insertMany([msg])
    		response.end(msg.Nombre)
    		}
    	);
	});
})

app.get('/nosotros/', function(request, response){
	response.render('nosotros.html');
})

app.get('/contactar/', function(request, response){

	response.render('contacto.html');

})

app.get('/como_funciona/', function(request, response){

	response.render('how_work.html');

})
app.get('/getGraphPerson/', function(request, response){

	var context={}

	var sender=function(cadena){
		redis.sendtoPython(
			function(result){
				list_nodes=[]
				list_links=[]
				cadena.forEach(function(element){
					for(node in element){
						if(list_nodes.findIndex(i => i.id == element[node]._id) == -1 && (node != 'r' && node != 'r2' && node != 'r3' && node != 'r4')){
							node_p={}
							node_p.id=element[node]._id
							node_p.labels=element[node].labels[0]
							node_p.url=element[node].properties.Url
							node_p.name=element[node].properties.name
							node_p.info='<div class="col-md-12 dont-break-out"><ul class="list-group">'
							for(subprop in element[node].properties){
								if(checkImageURL(element[node].properties[subprop])){
									node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+' <i class="fa fa-arrow-right" aria-hidden="true"></i>\
									            </strong><img style="object-fit: cover" class="avatar2" height = "70px" width="70px" src="'+element[node].properties[subprop]+'"></div></li>'
								}
								else if(ValidURL(element[node].properties[subprop])){
									node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+': </strong><a href="'+element[node].properties[subprop]+'" >'+element[node].properties[subprop]+'</a></div></li>'
								}
								else{
									if (element[node].properties[subprop].trim() != ""){
										node_p.info += '\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+': </strong>'+element[node].properties[subprop]+'</div></li>'
									}
								}
							}
							node_p.info+='</ul></div>'

							if (result[element[node].labels]!= undefined){
								node_p.group=hexToRgbA(result[element[node].labels[0]].style.color)
							}
							list_nodes.push(node_p)
						}else if (node == 'r' || node == 'r2' || node == 'r3' || node == 'r4'){
								element[node].forEach( function(element_r, index) {
									if(list_links.findIndex(i => i.id == element_r._id) == -1){
										link={}
										link.id=element_r._id
										link.type=element_r.type
										link.source=element_r._fromId
										link.target=element_r._toId
										link.info='<div class="col-md-12 dont-break-out"><ul class="list-group">'
										for(subprop in element_r.properties){
											link.info=link.info+'\n'+'<li class="list-group-item flex-column "><div class="d-flex w-10 justify-content-between"><strong>'+subprop.toUpperCase()+': </strong>'+element_r.properties[subprop]+'</div></li>'
										}
										link.info+='</ul></div>'

										list_links.push(link)

									}
								});


						}
					}
				})
				graph={}
				graph.nodes=list_nodes
				graph.links=list_links
				context.graph=JSON.stringify(graph)
				response.end(JSON.stringify(context))
			},'get getNode','getInfo nodeInfo')

	}
	neo4j.sendNeo4j(request.query.query,sender)
})

app.post('/send_message/', function(request, response){
	var transporter = nodemailer.createTransport({
	  service: properties.email.service,
	  auth: {
	    user: properties.email.name,
	    pass: properties.email.password
	  }
	});

	var mailOptions = {
	  from: properties.email.name,
	  to: properties.email.name,
	  subject: 'Mensaje de Contacto',
	  html: '<b>Email</b>: '+request.body.email+'<br>'+
	  		'<b>Nombre</b>: '+request.body.nombre+'<br><br>'+
	  		request.body.message

	};

	transporter.sendMail(mailOptions, function(error, info){
	  if (error) {
	    console.log(error);
	    response.end('fail')
	  } else {
	    console.log('Email sent: ' + info.response);
	    response.end('ok')
	  }
	});




})

function checkImageURL(url) {
    return(url.match(/\.(jpeg|jpg|gif|png|JPG)$/) != null);
}

function ValidURL(str) {
  var regex = /(http|https):\/\/(\w+:{0,1}\w*)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%!\-\/]))?/;
  if(!regex .test(str)) {
    //alert("Please enter valid URL.");
    return false;
  } else {
    return true;
  }
}
