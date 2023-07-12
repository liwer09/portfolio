import requests
import json
import re

#Definimos variables generales
headers = {"Authorization": "Bearer automation OLSMSABJRKIFDGS@G@YV","Accept": "application/json","Content-Type": "application/json"}
etag = ""

#Obtenemos el etag del host para poder modificarlo posteriormente, si no existe el etag significa que el host al que se esta atacando no existe, devolvemos un "failed" para realizar el filtrado de los que SI tienen etag.
def getetag(hostname):
    #Declaramos las variables de la peticion.
    global etag
    global headers
    url = "http://checkmk.central.cirsa.com/master/check_mk/api/1.0/objects/host_config/" + hostname
    #Mandamos la peticion.
    request = requests.get(url, headers=headers,verify=False)
    if request.status_code != 200:
        etag = ""
        return("failed")
    else:
        #Recogemos el valor de la peticion.
        return(request.headers.get("ETag"))

#Modificamos los hosts que tienen etag a traves de una request a la API
def modify_host_checkmk(etag, hostname):
    #Declaramos las variables de la peticion.
    url = "http://checkmk.central.cirsa.com/master/check_mk/api/1.0/objects/host_config/" + hostname
    headers = {"Authorization": "Bearer automation OLSMSABJRKIFDGS@G@YV","If-Match": etag,"Accept": "application/json","Content-Type": "application/json", }
    data=json.dumps({
        'update_attributes': {
            "tag_criticality": "prod"
        }
    })
    #Mandamos la peticion.
    request = requests.put(url, headers=headers, data=data, verify=False)
    if request.status_code == 200:
        print("Se ha modificado el host")
    else:
        print(request.content)
    #Aplicamos los cambios.
    url = "http://checkmk.central.cirsa.com/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke"
    requests.post(url, headers=headers)
    
#Aplica los cambios realizados en CheckMK   
def apply_changes():
    global headers
    requests.post("http://checkmk.central.cirsa.com/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke", headers=headers, verify=False)


if __name__ == '__main__':
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    hosts = input("Listado de hosts que van a ser modificados: \n")
    #Spliteamos el resultado para obtener una lista con todos los hosts como valores
    hosts = hosts.split(",")
    #Recorremos la lista y por host llamamos a la funcion "getetag" y "modify_host_checkmk" 
    for i in hosts:
        i = re.sub(" ","", i)
        etag = getetag(i)
        #Si no se obtiene el etag se pasa al siguiente host de la lista
        if "failed" in etag:
            print(f"failed {i}")
            continue
        else:
            modify_host_checkmk(str(etag), i)
    #Una vez todos los hosts se han modificado se llama a la funcion "apply_changes" para aplicar los cambios
    apply_changes()
            