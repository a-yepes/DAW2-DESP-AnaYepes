bind = "0.0.0.0:8000" #puerto donde escucha gunicorn (8000)

workers = 2 #numero de procesos worker que se ejecutan para manejar las solicitudes

timeout = 30 #tiempo max de espera

accesslog = "-"  #muestra peticiones recibidas

errorlog = "-" #muestra errores

capture_output = True #envia la salida de la aplicacion a los registros

loglevel = "info" # nivel de detalle de los logs