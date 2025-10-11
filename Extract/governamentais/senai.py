import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
url = "https://www.senairs.org.br/unidades-do-senai"
cards = []

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "view-content")))
    
    time.sleep(2)
    botao_cookies = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceito')]"))
    )
    botao_cookies.click()
    time.sleep(2)
    
    for i in range (1, 5):
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extrai os cards de cada unidade
        cards_full = soup.find_all("div", class_="fields-container")
        cards_full.pop(0)
        cards.extend(cards_full)
        if i != 4:
            # Clica no botão de próxima página
            next_button = driver.find_element(By.XPATH, "//a[@title='Ir para a próxima página']")
            next_button.click()
            time.sleep(2)
        

    # Cria o arq
    with open("senai_unidades.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Unidade", "Cidade"])

        for card in cards:
            nome = card.find("div", class_="views-field-title")
            cidade = card.find("span", class_="locality")

            nome_texto = nome.get_text(strip=True) if nome else ""
            cidade_texto = cidade.get_text(strip=True) if cidade else ""

            writer.writerow([nome_texto, cidade_texto])

    print(f"Total = {len(cards)}")

except Exception as e:
    print(f"Erro: {e}")

finally:
    driver.quit()
