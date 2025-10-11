import os

folder = 'reders\jsons_startups'
arq = "Serra_Gaucha.json"
complete_path = f"{folder}\\{arq}"

print(os.path.exists(complete_path), complete_path)