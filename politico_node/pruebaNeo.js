var neo4j = require('./neo4J.js');

neo4j.getEstructure({'Url':"https://es.wikipedia.org/wiki/Juan_Manuel_Santos"},
				function(structure){
					node = structure['p']
					console.log(node.properties)
				})
