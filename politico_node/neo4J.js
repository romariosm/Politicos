var properties = require('./properties.json')
var neo4j = require('neo4j');
module.exports = {
createNode: function (etiqueta,file){		
		sendNeo4j('create (p:' + etiqueta+' '+createParameters(file)+') return p')
	},
createRelation: function (tag_entidad_1,entidad_1,tag_entidad_2,entidad_2,tag){
 		sendNeo4j("CREATE ("+tag_entidad_1+" "+createParameters(entidad_1) +")-[:"+tag+"]->("+tag_entidad_2+" "+createParameters(entidad_2)+")")	
 	},
 getEstructure: function (url,level,callback){
 	sendNeo4j_2('match (p '+createParameters({'Url':url})+')-[r*1..'+level+']->(s) return p,r,s', callback)
 }
}
function sendNeo4j(sentence){	
	var db = new neo4j.GraphDatabase('http://' + properties.neo4j.user + ":" + properties.neo4j.password + "@" + properties.neo4j.host + ":"+properties.neo4j.port); 
		db.cypher({
    		query: sentence,
		}, function (err, results) {
    		if (err) throw err;
    		//.log(results)
    		var result = results[0];
    		//console.log(result);    		
		});	
}
function sendNeo4j_2(sentence,callback){	
	var db = new neo4j.GraphDatabase('http://' + properties.neo4j.user + ":" + properties.neo4j.password + "@" + properties.neo4j.host + ":"+properties.neo4j.port); 
		db.cypher({
    		query: sentence,
		}, function (err, results) {
    		if (err) throw err;
    		
    		var result = results[0];
    		callback(results)
    		//console.log(result);    		
		});	
}

function createRelation(tag_entidad_1,entidad_1,tag_entidad_2,entidad_2,tag){
 return "("+tag_entidad_1+" "+createParameters(entidad_1) +")-[:"+tag+"]->("+tag_entidad_2+" "+createParameters(entidad_2)+")"

}
function createParameters(json_file){
	var output = "{"
	for (key in json_file){
		output += key + ':"'+json_file[key]+'"'+","
	}
	return output.slice(0, output.length - 1) + "}"
	 
}


