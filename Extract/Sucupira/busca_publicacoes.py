import requests, json, os

api_url = "http://apigw-proxy.capes.gov.br/observatorio/data/catalogo/producao"
query = "ano-base:(2024);nome-grande-area-conhecimento:(CIÊNCIAS EXATAS E DA TERRA)"
size = 50
page, all_data = 0, []

while True:
    try:
        url = f"{api_url}?query={query}&page={page}&size={size}"
        r = requests.get(url)
        
        if r.status_code == 200:
            data = r.json()
            
            folder = "jsons_publicacoes"
            os.makedirs(folder, exist_ok=True)
            
            complete_path = os.path.join(folder, f"{page}.json")

            with open(complete_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            items = data.get("content", r)  # usa 'content' se existir, senão assume lista
            if not items:
                break
            all_data.extend(items)
            print(f"Página {page}: {len(items)} registros")
            page += 1
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

with open("publicacoes_sucup.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("Total salvo:", len(all_data))
