#El funcionamiento de este testing es obtener de una controladora Forti WLM los datos de las conexiones de los usuarios y llevaros a una BBDD para obtener el current status de conexiones por SSID y banda.

#Importamos las librerias
import time
import unittest
import psycopg2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#Llamamos a la clase de unittest
class PythonOrgSearch(unittest.TestCase):
    #Definimos las opciones necesarias para que funcione en Linux y creamos la variable del webdriver de Chrome
    def setUp(self):
        service = Service(executable_path=r'/usr/bin/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=service, options=options)


    def test_pt(self):
        #Definimos variables
        driver = self.driver
        wait = WebDriverWait(driver, 15)
        #Accedemos a la web y hacemos login, accedemos a los botones a través de XPATH porque comparten NAME e introducimos los datos a través de NAME porque es identificador unico.
        driver.get("URL")
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/form/button')))
        #Primer boton login
        driver.find_element(By.XPATH, '/html/body/div[1]/div/form/button').click()
        driver.find_element(By.NAME, 'username').send_keys("USER")
        driver.find_element(By.NAME, 'password').send_keys("PASSWORD")
        #Segundo boton login
        driver.find_element(By.XPATH,'/html/body/div[2]/div/form/button').click()
        #Accedemos a la web quitamos la primera pantalla del Netowrk health y esperamos a que cargue el elemento "Station" y le hacemos click para ver todas las conexiones
        #Flecha ocultar health status
        time.sleep(10)
        driver.find_element(By.XPATH, '/html/body/app-root/div[2]/div/div/div[1]/ul/li[5]/button/i').click()
        #Recuadro verde stations, wireless connections
        time.sleep(2)
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/section/div[2]/div/div/div/app-monitor-network/div[1]/div[1]/div[1]/div/div[2]/div/span/ul/li/ul/li/ul/li[2]/ul[1]")))
        stations = driver.find_element(By.XPATH, '/html/body/app-root/section/div[2]/div/div/div/app-monitor-network/div[1]/div[1]/div[1]/div/div[2]/div/span/ul/li/ul/li/ul/li[2]/ul[1]/li[1]')
        cantidad = stations.get_attribute("textContent")
        stations.click()
        a = 0
        #Dividimos la cantidad de host entre 10 que son los hosts mostrados en el listado y obtendremos la cantidad de veces a ejecutar el bucle para obtener datos y pasar pagina.
        cantidad_paginas = int(cantidad)/10
        #Limpiamos la tabla de la base de datos que utilizamos como "Current Status"
        conn = psycopg2.connect("host=10.146.67.18 dbname=wlm user=postgres password=u65r5c5U")
        cur = conn.cursor()
        cur.execute("DELETE FROM wlm;")
        conn.commit()
        cur.close()
        conn.close()
        #Hacemos un bucle para recoger los datos de los hosts por pagina y saltar a la siguiente
        while a <= int(cantidad_paginas):
            a = a + 1
            time.sleep(2)
            #Obtenemos las filas
            filas = driver.find_elements(By.CSS_SELECTOR, 'tr.mat-row')
            #Por cada fila creamos las variables y obtenemos las columnas
            for fila in filas:
                ap_name = ""
                banda = ""
                ssid = ""
                ssid_name = ""
                columnas = fila.find_elements(By.CSS_SELECTOR, 'td.mat-cell')
                i = 0
                #Por cada columna, vamos incrementando la variable i y por posicion vamos añadiendo contenido a las variables.
                for columna in columnas:
                    if i == 3:
                        ssid_name = columna.get_attribute("textContent")
                    elif i == 4:
                        ssid = columna.get_attribute("textContent")
                    elif i == 5:
                        banda = columna.get_attribute("textContent")
                    elif i == 8:
                        ap_name = columna.get_attribute("textContent")
                    i = i + 1
                #Enviamos los datos de la conexion a la tabla de nuestra base de datos
                conn = psycopg2.connect("host=10.146.67.18 dbname=wlm user=postgres password=u65r5c5U")
                cur = conn.cursor()
                cur.execute("INSERT INTO wlm(ap_name, banda, ssid, ssid_name) VALUES('%s', '%s', '%s', '%s');" %(str(ap_name), str(banda), str(ssid), str(ssid_name)))
                conn.commit()
                cur.close()
                conn.close()
            #Flecha siguiente pagina
            driver.find_element(By.XPATH,'/html/body/app-root/section/div[2]/div/div/div/app-monitor-network/div[2]/div/div/div[2]/div/serverside-pagination/mat-paginator/div/div/div[2]/button[2]').click()

    #Cuando falla o acaba cerramos la conexion
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()