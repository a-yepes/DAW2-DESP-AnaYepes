# Práctica 05

## 1. Introducción

En esta práctica he desarrollado y desplegado una aplicación web utilizando Docker Compose, Flask, MariaDB y Nginx.

He utilizado contenedores Docker para conservar los datos mediante volúmenes y realizar copias de seguridad y restauraciones de la base de datos.

El despliegue se ha realizado en la misma instancia EC2 de AWS que la práctica 4.

## 2. Tecnologías utilizadas

- **Docker:** plataforma para crear y ejecutar contenedores.
- **Docker Compose:** herramienta para definir y gestionar varios contenedores.
- **Flask:** framework de Python utilizado para desarrollar la aplicación web.
- **MariaDB:** sistema gestor de bases de datos relacional.
- **Nginx:** servidor web y proxy inverso.
- **AWS EC2:** servicio utilizado para alojar la aplicación.
- **Git y GitHub:** herramientas para controlar versiones y almacenar el proyecto.

## 3. Estructura del proyecto

La estructura de directorios y archivos es la siguiente:

```text
practica05-compose-mariadb/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── nginx/
│   └── nginx.conf
│
├── database/
│   ├── schema.sql
│   └── datos.sql
│
├── backups/
│   └── backup.sql
│
├── capturas/
│   ├── 01-estructura-proyecto.png
│   ├── 02-schema-sql.png
│   ├── 03-datos-sql.png
│   ├── 04-requirements.png
│   ├── 05-app-py.png
│   ├── 06-dockerfile.png
│   ├── 07-nginx.png
│   ├── 08-compose-yml.png
│   ├── 09-transferencia-ec2.png
│   ├── 10-zip-transferido.png
│   ├── 11-transferencia-verificada.png
│   ├── 12-compose-up.png
│   ├── 13-compose-ps.png
│   ├── 14-aplicacion-funcionando.png
│   ├── 15-acceso-mariadb.png
│   ├── 16-insert-mariadb.png
│   ├── 17-volumenes.png
│   ├── 18-backup-generado.png
│   ├── 19-borrar-datos.png
│   ├── 20-restaurar.png
│   └── 21-datos-restaurados.png
│
├── docs/
│   └── arquitectura-practica05.png
│
├── docker-compose.yml
├── README.md
└── requisitos.md
```

## 4. Arquitectura de la aplicación

La aplicación está formada por tres servicios principales:

1. **Nginx:** recibe las peticiones HTTP desde el navegador y las redirige a Flask.
2. **Flask:** procesa las peticiones y se comunica con MariaDB.
3. **MariaDB:** almacena la información de las tareas.

Los tres servicios se ejecutan en contenedores Docker y se comunican mediante una red interna de Docker.

MariaDB utiliza un volumen persistente para conservar los datos aunque los contenedores se detengan o se vuelvan a crear.

## 5. Configuración de Docker Compose

El archivo `docker-compose.yml` define los tres servicios:

- `nginx`
- `flask`
- `mariadb`

También configura:

- Una red interna para la comunicación entre contenedores.
- Un volumen persistente para los datos de MariaDB.
- Las variables de entorno necesarias para configurar la base de datos.
- Las dependencias entre servicios.
- Los puertos necesarios para acceder a la aplicación.

Para iniciar los servicios:

```bash
sudo docker-compose up -d
```

Para comprobar su estado:

```bash
sudo docker-compose ps
```

Para detener los servicios:

```bash
sudo docker-compose down
```

Este último comando conserva el volumen de datos porque no se utiliza la opción `-v`.

## 6. Despliegue en AWS EC2

He comprimido comprimido y transferido el proyecto desde el equipo local a la máquina virtual EC2 mediante SCP.

Una vez transferido, lo he descomprimido en el directorio:

```text
/opt/practica05/practica05-compose-mariadb
```

Posteriormente, he construido y arrancado los contenedores mediante Docker Compose.

He comprobado el funcionamiento de los servicios y el acceso a la aplicación a través del navegador utilizando la dirección IP pública de la instancia EC2.

## 7. Acceso a MariaDB

Para acceder al contenedor de MariaDB se utiliza:

```bash
sudo docker-compose exec mariadb mariadb -u root -p
```

Una vez dentro del sistema gestor de bases de datos, se selecciona la base de datos:

```sql
USE practica05AnaYepes;
```

Para consultar las tablas:

```sql
SHOW TABLES;
```

Para consultar los registros almacenados:

```sql
SELECT * FROM tareas;
```

## 8. Persistencia de datos mediante Docker Volume

La persistencia permite que los datos no desaparezcan cuando se detienen o eliminan los contenedores.

Para comprobarlo, se detienen los servicios:

```bash
sudo docker-compose down
```

Después se vuelven a iniciar:

```bash
sudo docker-compose up -d
```

Y accedemos de nuevo a MariaDB para comprobar que los registros de la tabla `tareas` siguen disponibles.

## 9. Copias de seguridad (Backup)

Para proteger la información almacenada en MariaDB he realizado una copia de seguridad utilizando `mariadb-dump`.

El comando utilizado es:

```bash
sudo docker-compose exec -T mariadb sh -c 'mariadb-dump -u root -p"$MARIADB_ROOT_PASSWORD" practica05AnaYepes' > backups/backup.sql
```

La copia se guarda en:

```text
backups/backup.sql
```

Este archivo contiene la estructura y los datos de la base de datos.

## 10. Restauración de datos (Restore)

Para comprobar la recuperación de la información se ha utilizado el archivo de copia de seguridad generado anteriormente.

El comando de restauración es:

```bash
sudo docker-compose exec -T mariadb sh -c 'mariadb -u root -p"$MARIADB_ROOT_PASSWORD" practica05AnaYepes' < backups/backup.sql
```

Una vez realizada la restauración, accedemos de nuevo a MariaDB y comprobamos que la tabla `tareas` contiene los registros recuperados:

```sql
USE practica05AnaYepes;
SHOW TABLES;
SELECT * FROM tareas;
```

## 11. Análisis de la arquitectura (Tarea 14)

### 1. ¿Qué problema resuelve Docker Compose?

Docker Compose permite definir y ejecutar aplicaciones formadas por varios contenedores mediante un único archivo de configuración. Facilita la administración, configuración y comunicación de los servicios.

En esta práctica permite gestionar conjuntamente Nginx, Flask y MariaDB sin tener que iniciar cada contenedor manualmente.

### 2. ¿Qué función desempeña Flask?

Flask es el servidor de aplicaciones web. Procesa las peticiones HTTP, se conecta a MariaDB, consulta los datos y devuelve la información al navegador.

En esta práctica actúa como intermediario entre el servidor web Nginx y la base de datos MariaDB.

### 3. ¿Qué función desempeña MariaDB?

MariaDB es el sistema gestor de bases de datos relacional. Almacena de forma organizada las tareas y permite realizar consultas, inserciones, modificaciones y eliminaciones.

En esta aplicación guarda la información que utiliza Flask para mostrar y gestionar las tareas.

### 4. ¿Por qué es necesaria Docker Network?

Docker Network permite que los contenedores se comuniquen entre sí mediante sus nombres de servicio, sin necesidad de exponer todos los puertos al exterior.

En esta práctica permite que Flask se conecte a MariaDB y que Nginx pueda comunicarse con Flask.

### 5. ¿Por qué es necesario Docker Volume?

Docker Volume permite conservar los datos de MariaDB aunque los contenedores se apaguen, se eliminen o se vuelvan a crear.

Es fundamental para evitar la pérdida de información cuando se reinicia o actualiza la aplicación.

### 6. ¿Por qué es importante Backup?

Backup permite crear una copia de seguridad de la información y protegerla ante posibles pérdidas, errores o fallos del sistema.

En esta práctica se utiliza `mariadb-dump` para generar el archivo `backup.sql`, que contiene una copia de la base de datos.

### 7. ¿Por qué es importante Restore?

Restore permite recuperar la información almacenada en una copia de seguridad cuando se produce una pérdida de datos.

En esta práctica se utiliza el archivo `backup.sql` para restaurar la base de datos y comprobar que los registros pueden recuperarse correctamente.


## 12. Problemas encontrados y soluciones
Al utilizar docker compose exec -T, aparecía un error porque no reconocía esa opción. Para solucionarlo he usado docker-compose con guión , que era la opción compatible con la versión instalada.

También con el archivo backup.sql, lo había generado en EC2 peor no me aparecía en local. Asi que he usado scp para descargar el archivo desde EC2 al ordenador y añadirlo al repositorio.

## 13. Conclusión

Con esta práctica he desplegado una aplicación web formada por varios servicios utilizando Docker Compose.

He trabajado con Flask como servidor de aplicaciones, MariaDB como sistema gestor de bases de datos y Nginx como proxy inverso.

También he configurado redes y volúmenes Docker, y transferido proyectos a una máquina virtual EC2.

Por último, he comprobado la importancia de realizar copias de seguridad y restauraciones para proteger la información y garantizar la persistencia de los datos.

