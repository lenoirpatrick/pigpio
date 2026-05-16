# pigpio
Monitoring d'un raspberrypi pour remonter les informations vers Home Assistant

![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-green.svg?style=flat&logo=python&logoColor=white)
![Home Assistant](https://img.shields.io/badge/Home_Assistant-2026.4-blue?style=flat&logo=homeassistant&logoColor=white)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=lenoirpatrick_pigpio&metric=bugs)](https://sonarcloud.io/summary/new_code?id=lenoirpatrick_pigpio)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=lenoirpatrick_pigpio&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=lenoirpatrick_pigpio)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=lenoirpatrick_pigpio&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=lenoirpatrick_pigpio)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=lenoirpatrick_pigpio&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=lenoirpatrick_pigpio)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lenoirpatrick_pigpio&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lenoirpatrick_pigpio)

[![GitHub stars](https://img.shields.io/github/stars/lenoirpatrick/pigpio?style=social)](https://github.com/lenoirpatrick/pigpio)
[![GitHub license](https://img.shields.io/github/license/lenoirpatrick/pigpio)](https://github.com/lenoirpatrick/pigpio)

# Installation
You should create a config.json file with :

```json
{
    "home_assistant": {
        "url": "http://{ha_ip_address}:{ha_port}/api/states/sensor.{sensor_name}",
        "token": "Bearer {ha_bearer_token}"
    },
    "domains_allowlist": ["{ha_ip_address}"]
}
```

- Bearer token can be created through _User > Security > Long term token_
- Sensors can be configured with configuration.yaml
- List of sensors
  - **raspberry_temperature** : actual temperature of the rpi (°C)
  - **raspberry_cpu_usage** : actual use of the CPU (%)
  - **raspberry_ram_usage** : actual use of the RAM (%)
  - **raspberry_disk_usage** : disk usage of the main partition (%)
  - **raspberry_cpu_date_maj** : date of update

```yaml
template:
- sensor:
    # PIGPIO
  - default_entity_id: sensor.raspberry_temperature
    unique_id: raspberry_temperature
    name: Température Raspberry
    state: '{{ state_attr(''sensor.raspberry_system'', ''temperature'') }}'
  - default_entity_id: sensor.raspberry_cpu_usage
    unique_id: raspberry_cpu_usage
    name: Usage CPU Raspberry
    state: '{{ state_attr(''sensor.raspberry_system'', ''cpu_usage'') }}'
  - default_entity_id: sensor.raspberry_ram_usage
    unique_id: raspberry_ram_usage
    name: Usage RAM Raspberry
    state: '{{ state_attr(''sensor.raspberry_system'', ''ram_usage'') }}'
  - default_entity_id: sensor.raspberry_disk_usage
    unique_id: raspberry_disk_usage
    name: Usage Disque Raspberry
    state: '{{ state_attr(''sensor.raspberry_system'', ''disk_usage'') }}'
  - default_entity_id: sensor.raspberry_cpu_date_maj
    unique_id: raspberry_cpu_date_maj
    name: Usage CPU Raspberry MAJ
    state: '{{ state_attr(''sensor.raspberry_system'', ''cpu_date_maj'') }}'
```

# Crontab
```
*/5 * * * * /usr/bin/python3 /path/to/pigpio/pigpio.py >> /path/to/pigpio/log.log 2>&1
```
