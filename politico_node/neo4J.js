var properties = require('./properties.json')
var neo4j = require('neo4j');
module.exports = {
 getEstructure: function (json,callback){
 	return sendNeo4j('match (p '+createParameters(json)+') RETURN p',callback)
 }
}
function sendNeo4j(sentence,callback){	
	var db = new neo4j.GraphDatabase('http://' + properties.neo4j.user + ":" + properties.neo4j.password + "@" + properties.neo4j.host + ":"+properties.neo4j.port); 
		db.cypher({
    		query: sentence,
		}, function (err, results) {
    		if (err) throw err;
    		var result = results[0];
    		callback(result)
		});			
}

function createParameters(json_file){
	var output = "{"
	for (key in json_file){
		output += key + ':"'+json_file[key]+'"'+","
	}
	return output.slice(0, output.length - 1) + "}"
	 
}


