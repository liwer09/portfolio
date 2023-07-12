import subprocess
import re

#Se requiere obtener la cantida de usuarios que estan conectados a una maquina Windows, para ello se ejecutaran sentencias en CMD y se recorrera el resultado de ellas.
def getallusers():
    #Declaramos variables necesarias durante el script
    totalusers = 0
    #Ejecutamos el comando query user que devuelve todos los usuarios, eliminamos todos los espacios sobrantes para poder hacer split y recorremos todas las lineas
    proc = subprocess.Popen("query user", stdout=subprocess.PIPE)
    users = proc.stdout.read()
    users = re.sub("  +","  ",str(users))
    users = users.split("\\r\\n")
    for line in users:
        line = line.split("  ")
        #Variara segun el idioma del sistema, si es en ingles se debe de hacer el if sobre "USERNAME", sino tambien se puede obviar la primera linea.
        if "NOMBRE USUARIO" in str(line):
            continue
        elif len(str(line).strip()) <= 5:
            continue
        else:
            totalusers = totalusers + 1
    if totalusers >= 5:
        print("WARNING - Se ha detectado que hay %s usuarios conectados a la maquina" % totalusers)
    else:
        print("OK - Se ha detectado que hay %s usuarios conectados a la maquina" % totalusers)

if __name__ == "__main__":
    getallusers()
