import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import OrderedDict

driver = webdriver.Firefox()
url = "https://sebrae.com.br/sites/PortalSebrae/canais_adicionais/contato_uf?codUf=22"
cidades = []
unidades = []
all_unids = []

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.ID, "main-content-front")))
    
    with open("sebrae.hmtl", "w", newline="", encoding="utf-8") as f:
        f.write(str(driver.page_source))
    
    botao_cookies = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    botao_cookies.click()
    time.sleep(2)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # Busca as cidades pra filtrar
    select = soup.find("select", {"id": "sbCidade"})
    if select:
        options = select.find_all("option")
        for option in options:
            if option.get("value") != "0":
                cidades.append(option.text.strip())
    
    # Objeto do filtro de cidade
    select_cidades = Select(driver.find_element(By.ID, "sbCidade"))
    for cidade in cidades:
        # Seleciona a cidade no filtro
        select_cidades.select_by_visible_text(cidade)
        # Busca e clica no pesquisar
        pesquisar_btn = driver.find_element(By.ID, "exibirContatos")
        pesquisar_btn.click()
        wait.until(EC.visibility_of_element_located((By.ID, "content-contato")))
        
        content = driver.page_source
        soup_content = BeautifulSoup(content, "html.parser")
        names_uni = soup_content.find_all("div", class_="sb-fale-conosco__sebrae-no-seu-estado__content__cidade__item__local")
        for namesu in names_uni:
            nome = namesu.find("h3").get_text(strip=True)
            all_unids.append([nome, cidade])
        
    for uni in all_unids:
        if uni not in unidades:
            unidades.append(uni)

    # Cria o CSV
    with open("sebrae_unidades.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Unidade", "Cidade"])

        for uni_nome, uni_cidade in unidades:
            writer.writerow([uni_nome, uni_cidade])

    print(f"Total = {len(unidades)}")

except Exception as e:
    print(f"Erro: {e}")

finally:
    driver.quit()
