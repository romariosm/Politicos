var properties = require('./properties.json')
var neo4j = require('neo4j');
module.exports = {
createNode: function (etiqueta,file){
		sendNeo4j('create (p:' + etiqueta+' '+createParameters(file)+') return p')
	}
}
function sendNeo4j(sentence){	
	var db = new neo4j.GraphDatabase('http://' + properties.neo4j.user + ":" + properties.neo4j.password + "@" + properties.neo4j.host + ":"+properties.neo4j.port); 
		db.cypher({
    		query: sentence,
		}, function (err, results) {
    		if (err) throw err;
    		var result = results[0];
    		console.log(result);    		
		});	
}
function createParameters(json_file){
	var output = "{"
	for (key in json_file){
		output += key + ':"'+json_file[key]+'"'+","
	}
	return output.slice(0, output.length - 1) + "}"
	 
}


