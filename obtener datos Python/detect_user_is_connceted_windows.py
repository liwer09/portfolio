import subprocess
import re

#Ejecutamos el comando "query user" en CMD y recorremos el output para visualizar si el usuario esta logeado.
def getallusers():
    user = "scadauser"
    #Declaramos variables necesarias durante el script.
    userdetected = 0
    #Ejecutamos el comando query user que devuelve todos los usuarios, eliminamos todos los espacios sobrantes para poder hacer split y recorremos todas las lineas.
    proc = subprocess.Popen("query user", stdout=subprocess.PIPE)
    users = proc.stdout.read()
    users = re.sub("  +","  ",str(users))
    users = users.split("\\r\\n")
    for line in users:
        line = line.split("  ")
        #Buscamos si en las lineas existe el usuario scadauser.
        if user in str(line):
            userdetected = 1
        else:
            continue
    #Si existe el usuario se marcara como OK, si no existe saltara un critical.
    if userdetected == 1:
        print("OK - El usuario %s tiene una sesion iniciada en la maquina" % (user))
    else:
        print("CRITICAL - El usuario %s no tiene una sesion iniciada en la maquina" % (user))

if __name__ == "__main__":
    getallusers()
