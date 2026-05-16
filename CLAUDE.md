# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

Script Python exécuté sur un Raspberry Pi qui collecte des métriques système (température CPU, usage CPU, RAM, espace disque de la partition principale `/dev/mmcblk0p2`) et les envoie à Home Assistant via son API REST.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install pylint

# Run the script
python pigpio.py

# Lint (mirrors CI)
pylint $(git ls-files '*.py')

# Run tests (if present)
pytest
```

## Architecture

- **`pigpio.py`** — script unique, trois responsabilités :
  1. `_get_system_metrics()` : collecte les métriques via des commandes shell Linux (`vcgencmd`, `top`, `free`, `df`). Retourne `{}` avec des valeurs vides si le système n'est pas Linux.
  2. `_send_to_home_assistant(data, config)` : envoie un POST vers l'API HA. La requête n'est effectuée que si le hostname de l'URL figure dans `DOMAINS_ALLOWLIST` (liste blanche anti-SSRF).
  3. `main()` : point d'entrée.

- **`config.json`** — gitignore, contient l'URL HA et le token Bearer, plus `domains_allowlist`. Un exemple de structure :
  ```json
  {
    "home_assistant": { "url": "...", "token": "Bearer ..." },
    "domains_allowlist": ["192.168.1.x"]
  }
  ```

## CI/CD

GitHub Actions (`.github/workflows/build.yml`) se déclenche sur `main` et `develop` :
- **SonarQube** — analyse qualité du code.
- **pylint** — testé sur Python 3.11, 3.12, 3.13.

## Key constraints

- `config.json` est gitignore ; il faut le créer manuellement avant d'exécuter le script.
- Les commandes shell de collecte (`vcgencmd`, etc.) ne fonctionnent que sur Linux/Raspberry Pi OS — les valeurs restent à `0` sur tout autre OS.
- La liste blanche `domains_allowlist` dans `config.json` doit contenir le hostname de l'URL HA pour que la requête soit envoyée.