var redis = require('redis')


var properties = require('./properties.json')

module.exports = {

sendRedis: function (callback,query,sub){	
	var redisClient = redis.createClient(properties.redis.port, properties.redis.host)
	redisClient.on('error',function(error){
		console.log("Se presentó un error con redis")
	})
	callback(redisClient,query,sub)
	redisClient.quit();
},

getSetRedis: function (redisClient,query,callback){
	redisClient.smembers(query, function(err,result){
		callback(result)
	})
},

getKeys: function (redisClient,query,callback){
	redisClient.keys(query, function(err,result){
		callback(result)
	})
},
hgetall: function (redisClient,query,callback){
	redisClient.hgetall(query, function(err,result){
		callback(result)
	})
},

sendtoPython: function (callback,emit,on){
	var socket = require('socket.io-client')('http://localhost:5000');
	socket.emit(emit)
	socket.on(on, function(result){
		callback(result)
	})	
},

getNodes: function (){
	sendtoPython(function(result){console.log(result.organization.relation.belongsTo)},'get getNode','getInfo nodeInfo')
}

}