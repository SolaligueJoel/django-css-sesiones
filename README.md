![Inove banner](inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---

# Django - css - sesiones
En este repositorio encontrarán los siguientes archivos:

__Ejemplos que el profesor mostrará en clase__\

* **dockerfile** (Para generar la imagen de Docker)
* **docker-compose.yml** (Para configurar el contenedor de Docker)
* **requirements.txt** (Que contiene las librerías que vamos a estar usando)
* **/marvel** (Directorio raíz de nuestra aplicación)
* **/database** (Directorio de nuestra base de datos)

---

# Comandos útiles 🐋

### 1. Correr el proyecto
Siempre en el mismo directorio del archivo *docker-compose.yml*
**$** `docker-compose up`

### 2. Correr la línea de comandos dentro del contenedor

**$** `docker exec -i -t modulo_4b bash`

Nos va a devolver a nuestra consola, una consola dentro del contenedor de software.


Una vez dentro ejecutamos el comando:

**$** `cd /opt/back_end/marvel` 