import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

categorias = ['2 A 5 MILHÕES', '5 A 30 MILHÕES', '30 A 150 MILHÕES', '150 A 300 MILHÕES', '300 A 600 MILHÕES', 'NOVATAS']

driver = webdriver.Firefox()
cabec = False

url = "https://exame.com/negocios-em-expansao/ranking"

try:
    with open('altoCresc.csv', "w", encoding="utf-8") as f:
        f.write("Unidade;Cidade" + '\n')
        for i in range(1, 6):
            # Busca já pela categoria na url pq não tava dando pra clicar nas abas
            driver.get(f"{url}/{i}/")
            wait = WebDriverWait(driver, 20)
            
            # Acha e clica no filtro de Sede
            sede_dropdown = wait.until(EC.element_to_be_clickable(
                (By.ID, "uf")
            ))
            driver.execute_script("arguments[0].click();", sede_dropdown)

            # Seleciona uf RS
            uf_rs = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//li[normalize-space()='RS']")
            ))
            driver.execute_script("arguments[0].click();", uf_rs)
            time.sleep(2)

            # Pega html pra conseguir os dados da tabela
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table')
            
            if not cabec:    
                # Cabeçalho
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                f.write("; ".join(headers) + '\n')
                cabec = True

            # Pega as empresas
            for row in table.find('tbody').find_all('tr'):
                cells = [td.get_text(strip=True) for td in row.find_all('td')]
                f.write("; ".join(cells) + '\n')

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    driver.quit()