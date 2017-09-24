var properties = require('./properties.json')
var neo4j = require('neo4j');
module.exports = {
 getEstructure: function (json,level,callback){
 	return sendNeo4j('match (p '+createParameters(json)+') RETURN p',callback)
 },
  getJul: function (json,callback){
 	return sendNeo4j('match (p '+createParameters(json)+')-[r:worksAt]->(q) RETURN q.name as inst,toInt(r.InicioJul) as ini,toInt(r.FinJul) as fin',callback)
 },
  getPartner: function (jsonI,inicio,fin,callback){
  	var rule = "(toInt(r.InicioJul) <= "+ inicio +" and toInt(r.FinJul) >= "+ fin +")"  +
	" or (toInt(r.InicioJul) >= "+ inicio +" and toInt(r.FinJul) >= "+ fin +" and toInt(r.InicioJul) <= "+ fin +")"+ 
	" or (toInt(r.InicioJul) <= "+ inicio +" and toInt(r.FinJul) <= "+ fin +" and toInt(r.FinJul) >= "+ inicio +")"
	return sendNeo4j('match all = (p)-[r:worksAt]->(q'+createParameters(jsonI)+') WHERE '+rule+' RETURN all',callback)
 }
}
function sendNeo4j(sentence,callback){	
	var db = new neo4j.GraphDatabase('http://' + properties.neo4j.user + ":" + properties.neo4j.password + "@" + properties.neo4j.host + ":"+properties.neo4j.port); 
		db.cypher({
    		query: sentence,
		}, function (err, results) {
    		if (err) throw err;
    		callback(results)
		});			
}

function createParameters(json_file){
	var output = "{"
	for (key in json_file){
		output += key + ':"'+json_file[key]+'"'+","
	}
	return output.slice(0, output.length - 1) + "}"
	 
}