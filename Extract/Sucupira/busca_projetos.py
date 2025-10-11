import requests, json, os

api_url = "http://apigw-proxy.capes.gov.br/observatorio/data/observatorio/projeto_pesquisa"
query = "ano-base:(2024);id-natureza-projeto:(1)"
size = 100
page, all_data = 0, []

while True:
    try:
        url = f"{api_url}?query={query}&page={page}&size={size}"
        r = requests.get(url)
        data = r.json()
        
        folder = "jsons_projetos"
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

with open("projetos_sucup.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("Total salvo:", len(all_data))