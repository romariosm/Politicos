var neo4j = require('./neo4J.js');

/*var a = neo4j.getEstructure({'Url':"https://es.wikipedia.org/wiki/Juan_Manuel_Santos"},
				function(structure){
					node = structure[0]['p']
					console.log(node.properties)
				})*/

neo4j.getJul({'Url':"https://es.wikipedia.org/wiki/Juan_Manuel_Santos"},function(structure){
	for (job in structure){
		neo4j.getPartner({name:structure[job].inst},
		structure[job].ini,
		structure[job].fin,				
		function(result){
			if (result.length > 0){
				console.log(result[0]['all'])
				} 
			}
		)
		}
	})