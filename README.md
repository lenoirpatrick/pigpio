# pigpio
Monitoring d'un raspberrypi

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
