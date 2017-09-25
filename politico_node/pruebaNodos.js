var redis = require('./pruebaRedis.js');
var neo4j = require('./neo4J.js');
var estructura;
var prueba = function(cadena){console.log(cadena)}
redis.sendtoPython(
			function(result){
				var nodos = result
				var level = 3
				var query = []
				for(key in nodos){
					for(subkey in nodos[key]['relation']){
						var subquery = nodos[key]['relation'][subkey].query.replace('?Url',"'https://es.wikipedia.org/wiki/Mar%C3%ADa_Clemencia_Rodr%C3%ADguez_de_Santos'")
						console.log(nodos[key]['relation'][subkey].scrolleable)
						if (nodos[key]['relation'][subkey].scrolleable == 1){
							query.push(subquery.replace('?scrolleable',level))
						}
						else{
							query.push(subquery)	
						}
						
					}
				}
				neo4j.sendNeo4j(query.join(' UNION ALL '),prueba)
		},'get getNode','getInfo nodeInfo')

