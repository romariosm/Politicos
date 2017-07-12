var neo4j = require('./neo4J.js');
module.exports = {
createPerson: function (structure){
		cleanPerson(structure)
		neo4j.createNode('Politic',structure)
	},
createParty: function (structure){	
		console.log(structure['name'])	
		neo4j.createNode('Party',structure['name'])
	},
createRelation:function(entidad_1,entidad_2,tag){
		cleanPerson(entidad_1)	
		neo4j.createRelation('Politic',entidad_1,'Party',entidad_2['name'],tag)
	},
getRelation:function(salida){
		neo4j.getRelation(salida)
	}
}

function cleanPerson(msg){
	for (var item in msg) {
  		if (typeof msg[item] === "object"){
  			msg[item] = msg[item].title
  		}
	}

}