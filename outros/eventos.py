from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

ecos={"Central" : "https://programainova.rs.gov.br/eventos-regiao-central",
    "Campanha e Fronteira Oeste": "https://programainova.rs.gov.br/eventos-regiao-fronteira-oeste-campanha",
    "Metropolitana e Litoral Norte": "https://programainova.rs.gov.br/eventos-regiao-metropolitana-litoral-norte",
    "Noroeste e Missões": "https://programainova.rs.gov.br/eventos-regiao-noroeste-missoes",
    "Produção e Norte": "https://programainova.rs.gov.br/eventos-regiao-producao-norte",
    "Serra Gaúcha": "https://programainova.rs.gov.br/eventos-regiao-serra-hortensias",
    "Sul": "https://programainova.rs.gov.br/eventos-regiao-sul",
    "Região dos Vales": "https://programainova.rs.gov.br/eventos-regiao-vales"
    
}

def get_eventos(file, ecossistema, url):
    driver.get(url)

    time.sleep(2)

    # Campo de Data Inicial
    campo_dta_inicial = driver.find_element(by=By.NAME, value="datahoraini")
    campo_dta_inicial.clear()
    campo_dta_inicial.send_keys("01/01/2025")
    campo_dta_inicial.send_keys(Keys.TAB)  # confirma a data

    time.sleep(3)

    # Clicar no botão Buscar
    filtrar = driver.find_element(By.XPATH, "//button[text()='Filtrar']")
    filtrar.click()

    # Esperar carregar os resultados
    time.sleep(2)

    html = BeautifulSoup(driver.page_source, "html.parser")

    for h2 in html.find_all("h2", class_="conteudo-lista__item__titulo"):
            for a in h2.find("a"):
                    file.write(ecossistema + ";" + a.string + ";" + "\n")


driver = webdriver.Firefox()
driver.maximize_window()

file_name = "eventos.csv"
        
with open(file_name, "w", encoding="utf-8") as f:
    for eco, url in ecos.items():
        get_eventos(f, eco, url)

driver.quit()