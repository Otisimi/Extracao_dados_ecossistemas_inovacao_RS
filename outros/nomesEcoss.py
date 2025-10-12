from bs4 import BeautifulSoup
from selenium import webdriver

# URL do inovaRS da pagina dos ecossistemas
URL = "https://programainova.rs.gov.br/ecossistemas-regionais"

# Uso Selenium pois página tem textos carregados por JS
driver = webdriver.Firefox()
driver.get(URL)

html = BeautifulSoup(driver.page_source, "html.parser")

with open ("ecossistemas_rs.csv", "w", encoding="utf-8") as f:
    for h2 in html.find_all("h2", class_="conteudo-lista__item__titulo"):
        for a in h2.find("a"):
                f.write(a.string + ";")
