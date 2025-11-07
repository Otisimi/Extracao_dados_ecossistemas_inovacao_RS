from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

ecos={"Central" : "https://programainova.rs.gov.br/eventos-regiao-central",
    "Fronteira Oeste e Campanha": "https://programainova.rs.gov.br/eventos-regiao-fronteira-oeste-campanha",
    "Metropolitana e Litoral Norte": "https://programainova.rs.gov.br/eventos-regiao-metropolitana-litoral-norte",
    "Noroeste e Missões": "https://programainova.rs.gov.br/eventos-regiao-noroeste-missoes",
    "Produção e Norte": "https://programainova.rs.gov.br/eventos-regiao-producao-norte",
    "Serra Gaúcha": "https://programainova.rs.gov.br/eventos-regiao-serra-hortensias",
    "Sul": "https://programainova.rs.gov.br/eventos-regiao-sul",
    "Vales": "https://programainova.rs.gov.br/eventos-regiao-vales"
    
}

btn_clicked = False

def extrair_data(texto):
    """Extrai apenas a data no formato DD/MM/YYYY do texto"""
    if not texto:
        return None
    
    # Procura por padrão DD/MM/YYYY
    match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', texto)
    if match:
        return match.group(1)
    return None

def get_eventos(file, ecossistema, url):
    global btn_clicked
    
    driver.get(url)
    time.sleep(5)
    # Cookies
    if not btn_clicked:
        btn_cookies = driver.find_element(by=By.ID, value="matriz2-cookie-confirmation-button")
        btn_cookies.click()
        btn_clicked = True
        time.sleep(5)
   
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
    eventos = html.find("div", class_="matriz-ui-pagedlist-body conteudo-lista__body")

    for evento in eventos.find_all("article", class_="conteudo-lista__item"):
        nome_ev = None
        dta_ini = None
        dta_fim = None
        # Nome do evento
        h2 = evento.find("h2", class_="conteudo-lista__item__titulo")
        if h2 and h2.find("a"):
            nome_ev = h2.find("a").string.strip()
        
        # Pegar as datas
        li_data = evento.find("li", class_="conteudo-lista__item__info-evento__data")
        if li_data:
            times = li_data.find_all("time")
            if len(times) == 2:
                dta_ini = extrair_data(times[0].get_text(strip=True))
                dta_fim = extrair_data(times[1].get_text(strip=True))
                # Se a segunda data não for válida, usar a primeira
                if dta_fim is None:
                    dta_fim = dta_ini
            elif len(times) == 1:
                # Evento de um dia só
                dta_ini = extrair_data(times[0].get_text(strip=True))
                dta_fim = dta_ini
        
        # Escrever no arquivo
        file.write(f"\n{ecossistema};{nome_ev};{dta_ini};{dta_fim}")


driver = webdriver.Firefox()
driver.maximize_window()

file_name = "eventos.csv"
        
with open(file_name, "w", encoding="utf-8") as f:
    f.write("Ecossistema;Evento;Data inicio;Data fim")
    for eco, url in ecos.items():
        get_eventos(f, eco, url)

driver.quit()