""" Script de récupération des informations d'un raspberrypi """

from datetime import datetime
import os
import json
import platform
import subprocess
from urllib.parse import urlparse
import requests

# Obtenir le répertoire courant du script exécuté
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin vers config.json
config_path = os.path.join(current_dir, "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    _config = json.load(f)

DOMAINS_ALLOWLIST = _config.get("domains_allowlist", [])


def _run_command(cmd):
    """Exécute une commande shell et retourne la sortie nettoyée."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def _get_system_metrics():
    """Récupère les métriques système (température, CPU, RAM)."""
    temp = 0.0
    cpu = 0.0
    ram = 0.0
    disk_usage = 0.0

    if platform.system() == "Linux":
        raw_temp = _run_command("vcgencmd measure_temp").replace("temp=", "").replace("'C", "")
        raw_cpu = _run_command("top -bn1 | grep \"Cpu(s)\" | awk '{print $2 + $4}'")
        raw_ram = _run_command("free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'")
        raw_disk = _run_command("df -h /dev/mmcblk0p2 | awk 'NR==2 {gsub(/%/,\"\"); print $5}'")

        temp = float(raw_temp) if raw_temp else 0.0
        cpu = float(raw_cpu) if raw_cpu else 0.0
        ram = float(raw_ram) if raw_ram else 0.0
        disk_usage = float(raw_disk) if raw_disk else 0.0

    cpu_date_maj = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "temperature": temp,
        "cpu_usage": cpu,
        "ram_usage": ram,
        "cpu_date_maj": cpu_date_maj,
        "disk_usage": disk_usage,
    }


def _send_to_home_assistant(data, config):
    """Envoie les données à Home Assistant."""
    url = config["home_assistant"]["url"]
    headers = {
        "Authorization": config["home_assistant"]["token"],
        "content-type": "application/json",
    }
    payload = {"state": True, "attributes": data}

    if urlparse(url).hostname not in DOMAINS_ALLOWLIST:
        return None

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi vers Home Assistant : {e}")
        return None


def main():
    """Point d'entrée principal du script."""
    metrics = _get_system_metrics()
    response = _send_to_home_assistant(metrics, _config)

    if response:
        print("Données envoyées :", metrics)
        print("Réponse du serveur :", response.status_code, response.text)


if __name__ == "__main__":
    main()
