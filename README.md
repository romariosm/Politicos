![alt text](https://github.com/romariosm/Politicos/blob/master/politico_node/static/images/logo2.png)

## ¿Qué es UMA UD?

Es un prototipo de software que permita identificar relaciones de pertenencia de personajes vinculados con la política colombiana utilizando un motor de bases de datos NoSQL, información pública en enciclopedias libres en el idioma español y procesamiento de lenguaje natural. 

## Estructura de UMA UD

La aplicación consta de:  
*	**Capa de datos:** donde se encuentran implementadas las bases de datos, MongoDB la cual se encarga de almacenar toda la información que extrae el aplicativo web de Wikipedia y Neo4j donde se guardadas todas las entidades y relaciones que fueron extraídas, luego de haber pasado por fases de procesamientos.
* **Capa de proceso:** 
   * La integración del crawler [Uru](https://github.com/romariosm/crawler). y la ontología. El crawler Uru extrae información personal, académica laboral y familiar de un determinado personaje de la política colombiana de Wikipedia, La ontología permite solucionar aspectos como el de sinonimia, modelo de datos dinámico, consultas a base de datos e información relacionada con la visualización de grafos. Dicha ontología fue implementada en REDIS, con el fin de optimizar los tiempos de respuesta 
   * Implementar un  servicio de socket que permite comunicar los procesos del sistema entre Python y NodeJS. 
* **Capa de presentación:** Contiene los flujos de trabajo entre el usuario y el aplicativo web por medio de las interfaces de usuario. 


![alt text](https://github.com/romariosm/Politicos/blob/master/politico_node/static/images/ArquitecturaTesis.png)
### ¿Cómo iniciar la aplicación? (Linux)

#### Archivos de configuración
La aplicación emplea dos archivos de configuración 

1. Archivo del Servicio Socket en python:

```sh
$ editor config.json
```
El cual cuenta con el siguiente contenido
```JSON
{
	"filePath": "python-service/Scrapy/Files/",
	"logFile":"UMAOntology.log",
	"loads":"python-service/Scrapy/Files/Cargues",
	"generatedFilePath":"python-service/Scrapy/Generated Files/",
	"databases":{
		"redis":{
			"host":"localhost",
			"port":6381,
			"db":0
		},
		"neo4j":{
			"host":"localhost",
			"port":7472,
			"auth":{
				"user":"neo4j",
				"psw": "1234"
			}
		}
	}
}
```
> **Nota:** La ubicación de este archivo varias según la manera en que se despliegue el servicio. 

2. Archivo de configuración de la aplicación en node 

```sh
$ editor politico_node/properties.json
```
El cual cuenta con el siguiente contenido
```JSON
{
	"mongo":{
		"host":"localhost",
		"port":27017,
		"database":"politicos",
		"collections":"personajes"
	},
	"redis":{
		"host":"localhost",
		"port":6381
	},
	"node":{
		"port":8082

	},
	"crawler":{
		"port":8083

	},
	"neo4j":{
		"host":"localhost",
		"port":7472,
		"user":"neo4j",
		"password":"1234"
	},
	"email":{
		"name":"rafasetienda@gmail.com",
		"password":"rafase123",
		"service":"gmail"
	}
}
```
#### Inicio base de datos Redis

Para ingresar las claves y valores necesarios para el funcionamiento de la aplicación ejecute el archivo `initOntology.py`
```sh
$ python python-service/Scrapy/initOntology.py
```
#### Servicio Python

Iniciar el entorno virtual
```sh
$ source politicos-env/bin/activate
```
Se debe asegurar que se encuentren instaladas todas las librerías necesarias para el funcionamiento del aplicativo. Las cuales se nombraran a continuación:

> adium-theme-ubuntu==0.3.4  
> beautifulsoup4==4.5.3  
> click==6.7  
> Flask==0.12  
> Flask-SocketIO==2.8.5  
> gyp==0.1  
> itsdangerous==0.24  
> Jinja2==2.9.5  
> MarkupSafe==1.0  
> pygobject==3.20.0  
> python-engineio==1.3.0  
> python-socketio==1.7.2 
> requests==2.13.0  
> six==1.10.0  
> unity-lens-photos==1.0  
> Werkzeug==0.12.1  
> wikipedia==1.4.0  

Para validar la librerías que se encuentran instaladas use el comando:
```sh
$ pip frezze 
```
Para instalar librerías faltantes utilice el comando:
```sh
$ pip install librería
```
Una vez se encuentre el entorno virtual configurado, diríjase a la carpeta en la que se encuentra el archivo para inciar el servicio:
```sh
$ cd python-service/Scrapy
```
Ejecute el archivo para iniciar el servicio
```sh
$ python socket_python.py 
```
> **Nota:** Debe tener en cuenta que para el inicio del servicio se debe haber previamente configurado las bases de datos (Redis y Neo4J) en el archivo de configuración. 

#### Iniciar la aplicación 

Para iniciar la aplicación en node basta con el comando:

```sh
$ node politico_node/server.js
```
