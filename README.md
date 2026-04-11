# pigpio
Monitoring d'un raspberrypi pour remonter les informations vers Home Assistant

![Python 3.11](https://img.shields.io/badge/python-3.11-green.svg?style=flat&logo=python&logoColor=white)
![Home Assistant](https://img.shields.io/badge/Home_Assistant-2026.4-blue?style=flat&logo=homeassistant&logoColor=white)

[![GitHub stars](https://img.shields.io/github/stars/lenoirpatrick/pigpio?style=social)](https://github.com/lenoirpatrick/pigpio)
[![GitHub license](https://img.shields.io/github/license/lenoirpatrick/pigpio)](https://github.com/lenoirpatrick/pigpio)

# Installation
You should create a config.json file with : 

```json
{
    "home_assistant": {
        "url": "http://{ha_ip_address}:{ha_port}/api/states/sensor.{sensor_name}",
        "token": "Bearer {ha_bearer_token}"
    }
}
```

- Bearer token can be create through _User > Security > Long term token_
- Sensors can be configured with configuration.yaml
- List of sensors
  - raspberry_temperature : actual temperature of the rpi
  - raspberry_cpu_usage : actual use of the CPU
  - raspberry_ram_usage : actual use of the RAM
  - raspberry_cpu_date_maj : date of update
``` yaml
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
  - default_entity_id: sensor.raspberry_cpu_date_maj
    unique_id: raspberry_cpu_date_maj
    name: Usage CPU Raspberry MAJ
    state: '{{ state_attr(''sensor.raspberry_system'', ''cpu_date_maj'') }}'
    
# PIGPIO
rest_command:
  update_raspberry_stats:
    url: "http://{ha_ip_address}:{ha_port}/api/states/sensor.raspberry_system"
    method: POST
    headers:
      content-type: application/json
    payload: >
      {
        "state": "ok",
        "attributes": {
          "temperature": "{{ temperature }}",
          "cpu_usage": "{{ cpu_usage }}",
          "ram_usage": "{{ ram_usage }}"
        }
      }
```

# Crontab
```
*/5 * * * * /usr/bin/python3 /home/pi/app/pigpio/pigpio.py >> /home/pi/app/pigpio/log.log 2>&1
```