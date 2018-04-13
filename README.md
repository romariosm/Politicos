# UMA UD 

¿Qué es UMA UD?

## Estructura de UMA UD

¿Cómo es la estructura del proyecto?

### ¿Cómo iniciar la aplicación? (Linux)

#### Servicio Python

Iniciar el entorno virutal
```console
source politicos-env/bin/activate
```
Se debe asegurar que se encuentren instaladas todas las librerías necesarias para el funcionamiento del aplicativo. Las cuales se nombraran a continuación:
```
adium-theme-ubuntu==0.3.4
beautifulsoup4==4.5.3
click==6.7
Flask==0.12
Flask-SocketIO==2.8.5
gyp==0.1
itsdangerous==0.24
Jinja2==2.9.5
MarkupSafe==1.0
pygobject==3.20.0
python-engineio==1.3.0
python-socketio==1.7.2
requests==2.13.0
six==1.10.0
unity-lens-photos==1.0
Werkzeug==0.12.1
wikipedia==1.4.0
```
Para validar la librerías que se encuentran instaladas use el comando:
```console
pip frezze 
```
Para instalar librerías faltantes utilice el comando:
```console
pip install librería
```
Una vez se encuentre el entorno virtual configurado, diríjase a la carpeta en la que se encuentra el archivo para inciar el servicio:
```console
cd python-service/Scrapy
```
Ejecute el archivo para iniciar el servicio
```console
python socket_python.py 
```

