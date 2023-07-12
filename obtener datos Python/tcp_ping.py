#Importamos librerias
import socket
import sys
from datetime import datetime

'''Realizamos una conexion a traves de un socket AF_INET, si la conexion devuelve un connection refused (la maquina rechaza la conexion) o recibimos una conexion valida, marcaremos como UP el host, si recibimos un
timeout marcaremos el host como DOWN.'''
def ping(ip, puerto):
    #Spliteamos los puertos para pasarlos a una lista y poderlos reccorer
    puerto = str(puerto).split(" ")
    #Por cada puerto del listado verificaremos si da refused, ok o timeout, si devuelve refused o OK pararemos si da timeout continuamos con el resto de puertos.
    for port in puerto:
        #Hacemos un try para poder identificar los errores con el except.
        try:
            #Creamos el socket para hacer la conexion al puerto correcto
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Definimos el timeout
            sock.settimeout(5) 
            #Lanzamos la conexion y si devuelve refused es OK, si devuelve timeout es NOK, aparte obtenemos la fecha actual y la restamos para obtener el Round Trip.
            tiempo_inicial = datetime.now()
            sock.connect((ip, int(port)))
            tiempo_final = datetime.now()
            rta = ((tiempo_final - tiempo_inicial).total_seconds() * 1000)
            print("OK - Ha tardado %s ms. | rta=%s" % (str(int(rta)), str(int(rta))))
            sys.exit(0)
        except ConnectionRefusedError as e:
            tiempo_final = datetime.now()
            rta = ((tiempo_final - tiempo_inicial).total_seconds() * 1000)
            print("OK - Ha tardado %s ms. | rta=%s" % (str(int(rta)), str(int(rta))))
            sys.exit(0)
        except socket.timeout:
            error = 1
    #Si todos los puertos fallan devolvemos un critical.
    if error == 1:
        print("CRITICAL - El dispositivo no esta disponible.")
        sys.exit(2)

if __name__ == "__main__":
    ping(sys.argv[1], sys.argv[2])