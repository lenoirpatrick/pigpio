import os
import json
import requests

def get_system_metrics():
    """Récupère les métriques système (température, CPU, RAM)."""
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
    return {"temperature": temp, "cpu_usage": cpu, "ram_usage": ram}

def send_to_home_assistant(data, config):
    """Envoie les données à Home Assistant."""
    url = config["home_assistant"]["url"]
    headers = {
        "Authorization": config["home_assistant"]["token"],
        "content-type": "application/json",
    }
    payload = {"state": "ok", "attributes": data}
    response = requests.post(url, headers=headers, json=payload)
    return response

def main():
    """Point d'entrée principal du script."""
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    metrics = get_system_metrics()
    response = send_to_home_assistant(metrics, config)

    print("Données envoyées :", metrics)
    print("Réponse du serveur :", response.status_code, response.text)

if __name__ == "__main__":
    main()