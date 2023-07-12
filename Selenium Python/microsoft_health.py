#Importamos las librerias
import requests
import unittest
from selenium import webdriver
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
        #chr_options.add_argument("--start-maximized")
        chr_options.add_argument("--headless")
        self.driver = webdriver.Chrome(driver_path, options=chr_options)

    #Enviar datos al OBM de microfocus
    def send_omi(text, origen):
        last_line = ""
        f = open("/opt/selenium/log_" + origen + ".log", "a")
        for line in f:
            last_line = line
        if (text in last_line):
            pass
        else:    
            if (text == "Available"):
                body = "<event><description>OK: " + text + "</description><severity>NORMAL</severity><nodo>Microsoft Status</nodo><category>" + origen + "</category><subcategory>Health</subcategory><fuente>Microsoft</fuente><type>Performance</type></event>"
                requests.post("OBM_URL", data=body, verify=False)
            else:
                body = "<event><description>CRIT: " + text + "</description><severity>CRITICAL</severity><nodo>Microsoft Status</nodo><category>" + origen + "</category><subcategory>Health</subcategory><fuente>Microsoft</fuente><type>Performance</type></event>"
                requests.post("OBM_URL", data=body, verify=False)

    def test_pt(self):
        #Definimos las variables
        driver = self.driver
        #Accedemos a la web
        driver.get("https://status.office365.com/")
        #Enviamos a la funcion send_omi el valor del elemento de la web donde indica el estado del servicio de Azure y O365
        send_omi(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div/div[2]/div[1]/div[2]/span"))).get_attribute("textContent"), "o365")
        send_omi(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/section/div/div/div/div/div[2]/div[2]/div[2]/span"))).get_attribute("textContent"), "azure")

    #Si falla o acaba cerramos el navegador abierto por el driver
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    #Llamamos a la clase de unittest
    unittest.main()