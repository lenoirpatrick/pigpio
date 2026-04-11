import os
import json
import platform
import requests
from datetime import datetime
from urllib.parse import urlparse

# Obtenir le répertoire courant du script exécuté
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin vers config.json
config_path = os.path.join(current_dir, "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    _config = json.load(f)

DOMAINS_ALLOWLIST = _config.get("domains_allowlist")

def _get_system_metrics():
    """Récupère les métriques système (température, CPU, RAM)."""
    temp = 0
    cpu = 0
    ram = 0

    # Récupère le nom du système d'exploitation
    os_type = platform.system()

    if os_type == "Linux":
        temp = (
            os.popen("vcgencmd measure_temp")
            .readline()
            .replace("temp=", "")
            .replace("'C\n", "")
        )
        cpu = (
            os.popen("top -bn1 | grep \"Cpu(s)\" | awk '{print $2 + $4}'")
            .readline()
            .strip()
        )
        ram = (
            os.popen("free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'")
            .readline()
            .strip()
        )
    # Remplace "demo" par la date actuelle
    cpu_date_maj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"temperature": temp, "cpu_usage": cpu, "ram_usage": ram, "cpu_date_maj": cpu_date_maj}

def _send_to_home_assistant(data, config):
    """Envoie les données à Home Assistant."""
    url = config["home_assistant"]["url"]
    headers = {
        "Authorization": config["home_assistant"]["token"],
        "content-type": "application/json",
    }
    payload = {"state": True, "attributes": data}

    if urlparse(url).hostname in DOMAINS_ALLOWLIST:
        response = requests.post(url, headers=headers, json=payload)
    else:
        response = None
    return response

def main():
    """Point d'entrée principal du script."""

    metrics = _get_system_metrics()
    response = _send_to_home_assistant(metrics, _config)

    if response:
        print("Données envoyées :", metrics)
        print("Réponse du serveur :", response.status_code, response.text)

if __name__ == "__main__":
    main()