# Práctica 06

## 1. Introducción

En esta práctica he trabajado con Terraform para automatizar el aprovisionamiento de infraestructura en AWS.

## 2. Terraform

Terraform es una herramienta de Infrastructure as Code que permite definir y administrar recursos de infraestructura mediante archivos de configuración.

Contiene los archivos:

- `main.tf`: define el proveedor AWS, la instancia EC2 y el Security Group.
- `variables.tf`: define las variables utilizadas.
- `outputs.tf`: muestra información de los recursos creados.

## 3. AWS

AWS (Amazon Web Services) es una plataforma de servicios cloud.

He utilizado Amazon EC2 para desplegar una máquina virtual Ubuntu Server.

## 4. Infrastructure as Code

Infrastructure as Code permite gestionar la infraestructura mediante código en lugar de realizar configuraciones manuales.

Sus principales ventajas son la automatización, la reproducibilidad y la facilidad de mantenimiento.

## 5. Configuración realizada

He configurado Terraform para trabajar con AWS mediante credenciales temporales de AWS Academy.

Después, he definido una instancia EC2 con Ubuntu Server y tipo de instancia t2.micro.

En una segunda modificación he incorporado un Security Group con las reglas de acceso SSH, HTTP y HTTPS.

También he asociado la Key Pair `practica04` para permitir el acceso mediante SSH.

## 6. Recursos creados

- Una instancia EC2.
- Un Security Group.
- Reglas de entrada para SSH, HTTP y HTTPS.
- Reglas de salida.
- Asociación de una Key Pair.

## 7. Problemas encontrados y soluciones aplicadas

En la primera configuración, la instancia EC2 no tenía Key Pair propia ni de un Security Group específico.

Para solucionarlo he modificado el Security Group en Terraform y configurado las reglas de acceso. También he asociado la Key Pair `practica04` a la instancia.

Otro problema que he encontrado es que había introducido por error la carpeta .terraform en un git push. La carpeta contenía el proveedor AWS y pesaba mucho. Como Github no permite subir archivos de más de 100 MB me daba error. 

Para solucionarlo he utilizado git-filter-repo, para eliminarlos del historial de Git. Finalmente, volví a subir el repositorio utilizando git push --force-with-lease.


## 8. Conclusiones

Esta práctica demuestra cómo Terraform facilita la automatización de infraestructura en AWS.

He podido  inicializar, validar, planificar y aplicar configuraciones, además de crear una instancia EC2 y gestionar sus reglas de seguridad.

La utilización de Infrastructure as Code permite crear infraestructuras reproducibles y reduce la necesidad de realizar configuraciones manuales.

## Limitaciones de la infraestructura inicial

En la primera versión de Terraform se ha creado
una instancia EC2 en AWS.

Sin embargo, la infraestructura todavía está
incompleta porque:

- No se ha asociado una Key Pair.
- No se ha creado un Security Group propio.
- No se han configurado las reglas de acceso SSH.
- No se han configurado las reglas HTTP y HTTPS.

Por tanto, es necesario ampliar la configuración
de Terraform para permitir la administración
remota de la instancia.


# TAREA 12. Análisis final


## Infrastructure as Code

- ¿Qué significa?
  
- Infrastructure as Code (Infraestructura como Código) consiste en crear y administrar infraestructuras informáticas mediante archivos de configuración y código, en lugar de hacerlo todo manualmente desde una consola. De esta forma, podemos definir qué recursos necesitamos y cómo deben configurarse.

## Terraform

- ¿Qué ventajas aporta frente a la creación manual de recursos?

- Terraform permite crear y gestionar recursos de forma automática, rápida y organizada. Además, podemos reutilizar los mismos archivos de configuración para desplegar infraestructuras similares sin tener que repetir todos los pasos manualmente. También facilita detectar cambios y mantener una configuración consistente.

## Security Groups

- ¿Qué función desempeñan?
  
- Los Security Groups funcionan como un cortafuegos virtual para las instancias EC2. Permiten controlar el tráfico de entrada y salida, indicando qué conexiones están permitidas. En esta práctica hemos configurado los puertos 22 (SSH), 80 (HTTP) y 443 (HTTPS) para permitir el acceso correspondiente al servidor.

## Key Pairs

- ¿Por qué son necesarias?
  
- Las Key Pairs permiten conectarnos de forma segura a una instancia EC2 mediante SSH. Están formadas por una clave pública, que se configura en AWS, y una clave privada, que debemos conservar en nuestro ordenador. En esta práctica hemos utilizado el par de claves practica04 para acceder a la instancia.

## terraform init

- ¿Para qué sirve?
  
- El comando terraform init prepara el proyecto para poder trabajar con Terraform. Descarga los proveedores necesarios, como el de AWS, e inicializa el directorio de trabajo para poder ejecutar los siguientes comandos.

## terraform plan

- ¿Para qué sirve?
  
- El comando terraform plan muestra los cambios que Terraform va a realizar en la infraestructura. Permite comprobar qué recursos se van a crear, modificar o eliminar antes de aplicar los cambios.

## terraform apply

- ¿Para qué sirve?
- 
- El comando terraform apply ejecuta los cambios definidos en los archivos de configuración y crea o modifica los recursos en AWS. En esta práctica lo hemos utilizado para desplegar la instancia EC2 y configurar su Security Group y su Key Pair.

## terraform destroy

- ¿Para qué sirve?
  
- El comando terraform destroy elimina los recursos que Terraform ha creado y que están registrados en su estado. Es útil para limpiar los recursos cuando ya no son necesarios y evitar seguir consumiendo recursos de AWS.

## Automatización

- ¿Qué ventajas presenta Terraform para equipos DevOps?
  
- Terraform facilita el trabajo de los equipos DevOps porque permite compartir archivos de configuración, trabajar de forma organizada y mantener las infraestructuras controladas mediante versiones con Git. También ayuda a automatizar los despliegues, reducir errores humanos y repetir configuraciones en diferentes entornos.
  

## Automatización

- ¿Qué ventajas presenta frente a la creación manual de recursos?
  
- Frente a la creación manual, Terraform ahorra tiempo y evita tener que configurar cada recurso paso a paso desde la consola de AWS. Además, permite repetir los despliegues de manera sencilla, mantener una configuración uniforme y revisar los cambios antes de ejecutarlos. Esto hace que la gestión de la infraestructura sea más rápida, sencilla y fiable.


