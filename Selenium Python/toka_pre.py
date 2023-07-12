#Importamos las librerias
import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Llamamos a la clase unittest
class PythonOrgSearch(unittest.TestCase):
    #Definimos las opciones y creamos la variable del webdriver 
    def setUp(self):
        driver_path = "C:\DRIVERS\driverchrome.exe"
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        chr_options.add_argument("--start-maximized")
        #chr_options.add_argument("--headless")
        self.driver = webdriver.Chrome(driver_path, options=chr_options)

    def test_pt(self):
        #Definimos las variables
        driver = self.driver
        #Obtenemos el tiempo para sacar la performance de la web.
        t0 = time.time()
        #Accedemos a la web.
        driver.get("https://toka-dev.central.cirsa.com")
        #Esoeranis a que el elemento HTML indicado sea visible
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/main/div/section/div/div/div[1]/div/div[1]/div/div[1]/h1")))
        #Obtenemos la segunda marca de tiempo y hacemos la resta
        t1 = time.time()
        tiempoinforme = t1 - t0
        #Guardamos en un log el tiempo de carga.
        log = open(r'C:\DRIVERS\\toka_pre.log',"a")
        log.write(str(time.ctime()) + " - Ha tardado " + str(tiempoinforme) + "s en cargar el informe \n") 
        log.close()

    #Si falla o acaba cerramos el navegador
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    #Llamamos a la clase unittest
    unittest.main()