from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Carregando variaveis de ambiente
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
url      = os.getenv("URL")

# Define paths para recursos externos
driver_path = "./driver/chromedriver-linux64/chromedriver"
chromium_binary_path = "/usr/bin/chromium"

# configura opcoes do driver
chrome_options = Options()
chrome_options.binary_location = chromium_binary_path

# Bloqueia camera e microfone por padrao
prefs = {
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.media_stream_mic": 2,
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializando o navegador
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acessando a URL
driver.get(url)

# Aguarde a página carregar (depende da sua conexão)
time.sleep(3)

# Localizando o campo do código
codigo_field = driver.find_element(By.ID, "codigoEmpregador")
codigo_field.send_keys(username)

# Localizando o campo do PIN
pin_field = driver.find_element(By.ID, "codigoPin")
pin_field.send_keys(password)

# Localizando o botão de registrar e clicando
registrar_button = driver.find_element(By.ID, "registraPonto")
registrar_button.click()

time.sleep(3)

# Fechar o navegador
driver.quit()

