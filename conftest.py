"""Configuration pytest : mock config.json pour permettre l'import de pigpio sans fichier réel."""
from unittest.mock import patch

_TEST_CONFIG = {
    "home_assistant": {
        "url": "http://192.168.1.1:8123/api/states/sensor.test",
        "token": "Bearer test_token",
    },
    "domains_allowlist": ["192.168.1.1"],
}

with patch("builtins.open"), patch("json.load", return_value=_TEST_CONFIG):
    import pigpio  # noqa: E402  # pylint: disable=wrong-import-position,unused-import
