var redis = require('redis')


var properties = require('./properties.json')

function sendRedis(callback,query,sub){	
	var redisClient = redis.createClient(properties.redis.port, properties.redis.host)
	redisClient.on('error',function(error){
		console.log("Se presentó un error con redis")
	})
	callback(redisClient,query,sub)
	redisClient.quit();
}

function getSetRedis(redisClient,query,callback){
	redisClient.smembers(query, function(err,result){
		callback(result)
	})
}

function getKeys(redisClient,query,callback){
	redisClient.keys(query, function(err,result){
		callback(result)
	})
}
function hgetall(redisClient,query,callback){
	redisClient.hgetall(query, function(err,result){
		callback(result)
	})
}

function sendtoPython(callback,emit,on){
	var socket = require('socket.io-client')('http://localhost:5000');
	socket.emit(emit)
	socket.on(on, function(result){
		callback(result)
	})	
}


function getNodes(){
	sendtoPython(function(result){console.log(result)},'get getNode','getInfo nodeInfo')
}

getNodes()