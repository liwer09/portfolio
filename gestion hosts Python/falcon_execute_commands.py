#!/usr/bin/env python
# Librerias a importar
import logging # Requiere instalacion
from falconpy import APIHarness, Hosts, RealTimeResponseAdmin # Requiere instalacion
from getpass import getpass
import requests
import socket
import json
import re
import time
#Variables globales
client = ""
secret = ""

#Con esta función vemos el output que nos da los comandos ejecutados para obtener la version de los sistemas Linux y si estan utilizando un daemon initctl
def distribution(request_id, seelegacy, host):
    global client
    global secret
    falcon = RealTimeResponseAdmin(client_id=client, client_secret=secret)
    response = falcon.check_admin_command_status(cloud_request_id=request_id)
    if "200" in str(response["status_code"]):
        result = response["body"]["resources"][0]["stdout"]
        result = result.split("\n")
        for i in result:
            print(i)
        result = response["body"]["resources"][0]["stderr"]
        result = result.split("\n")
        for i in result:
            print(i)


#Enviamos los comandos necesarios para validar la version y el daemon utilizado
def sendcommanddistribution(consoleid, hostid, host, command):
    global client
    global secret
    command_string = f"runscript -Raw=```{command}```"
    falcon = RealTimeResponseAdmin(client_id=client, client_secret=secret)
    response = falcon.execute_admin_command(session_id=consoleid,base_command="runscript",command_string=command_string)
    if "201" in str(response["status_code"]):
        request_id = response["body"]["resources"][0]["cloud_request_id"]
        return request_id

# Funcion para crear el ID de la consola para poder ejecutar los comandos.
def createconsole(hostid, host):
    global client
    global secret
    print("\n Obteniendo el consoleID del host %s." % (host))
    falcon = APIHarness(creds={'client_id': client, 'client_secret': secret})
    body = {'device_id': hostid[0]}
    response = falcon.command(action='RTR-InitSession', body=body)
    if "201" in str(response["status_code"]):
        sessionid = response["body"]["resources"][0]["session_id"]
        if len(sessionid) != 0:
            return sessionid
        else:
            print("\nNo se ha podido obtener el ID.")
            logging.warning("%s No tiene crowdstrike" % (host))
            return "failed"
    else:
        logging.warning("%s No tiene crowdstrike" % (host))
        return "failed"

# Funcion para obtener los IDs de los hosts a partir del hostname.
def gethost(hostname):
    global client
    global secret
    print("\n Obteniendo el ID del host %s." % (hostname))
    falcon = Hosts(client_id=client, client_secret=secret)
    response = falcon.query_devices_by_filter(filter=f"hostname:*'*{hostname}*'")
    if "200" in str(response["status_code"]):
        hostid = response["body"]["resources"]
        if len(hostid) != 0:
            return hostid
        else:
            logging.warning("%s No tiene crowdstrike" % (hostname))
            return "failed"
    else:
        logging.warning("%s No tiene crowdstrike" % (hostname))
        return "failed"
            

# Funcion para ver la version de los servidores linux.
def executecommand(host, command):
    host = host.split(",")
    for i in host:
        i = re.sub(' ','', i)
        hostid = gethost(i)
        if not "failed" in str(hostid):
                consoleid = createconsole(hostid, i)
                if not "failed" in str(consoleid):
                    request_id = sendcommanddistribution(consoleid, hostid, i, command)
                    if not "failed" in str(request_id):
                        distribution(request_id, "0", i)
                else:
                    print("Failed")
        else:
            print("Failed")
                

def menu():
# Funcion menú
    a = 0
    while a < 1:
        accion = input("1. Ejecutar comando. \n 2. Cerrar aplicación. \n\nIntroduce la opción a escoger: ") 
        if accion == "1":
            host = input("\n Indica los hostname (si se añaden varios se debe de usar una , para separarlos): ")
            command = input("\n Indica el comando a ejecutar: ")
            executecommand(host, command)

        elif accion == "2":
            logging.info("Cerrando el programa.")
            print("Se cerrara el aplicativo.")
            a = 1
        else:
            print("No se ha escogido una opcion correcta.")

# Función para obtener los datos de conexion a la API
def getclient():
    global client
    global secret
    client = input("\nIndica el client ID: ")
    secret = getpass(prompt='\nIndica el client secret: ')


# Inicializacion de la aplicacion
if __name__ == "__main__":
    logging.basicConfig(filename='log_info.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    logging.info("Iniciando el programa.")
    getclient()
    menu()