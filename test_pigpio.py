"""Tests unitaires pour pigpio.py."""
from datetime import datetime
from unittest.mock import patch, MagicMock
import platform
import requests
import pigpio


_TEST_CONFIG = {
    "home_assistant": {
        "url": "http://192.168.1.1:8123/api/states/sensor.test",
        "token": "Bearer test_token",
    }
}


class TestGetSystemMetrics:
    """Tests pour _get_system_metrics."""

    def test_returns_expected_keys(self):
        """Vérifie que toutes les clés attendues sont présentes."""
        metrics = pigpio._get_system_metrics()  # pylint: disable=protected-access
        expected = {"temperature", "cpu_usage", "ram_usage", "cpu_date_maj", "disk_usage"}
        assert set(metrics.keys()) == expected

    def test_returns_floats_on_non_linux(self):
        """Vérifie que les valeurs par défaut sont des floats sur un OS non-Linux."""
        with patch.object(platform, "system", return_value="Windows"):
            # pylint: disable=protected-access
            metrics = pigpio._get_system_metrics()
        assert isinstance(metrics["temperature"], float)
        assert isinstance(metrics["cpu_usage"], float)
        assert isinstance(metrics["ram_usage"], float)
        assert isinstance(metrics["disk_usage"], float)

    def test_date_format(self):
        """Vérifie que cpu_date_maj respecte le format attendu."""
        metrics = pigpio._get_system_metrics()  # pylint: disable=protected-access
        datetime.strptime(metrics["cpu_date_maj"], "%Y-%m-%d %H:%M:%S")


class TestSendToHomeAssistant:
    """Tests pour _send_to_home_assistant."""

    def test_does_not_send_if_domain_not_in_allowlist(self):
        """Vérifie qu'aucune requête n'est envoyée si le domaine n'est pas dans la whitelist."""
        with patch.object(pigpio, "DOMAINS_ALLOWLIST", []):
            with patch("pigpio.requests.post") as mock_post:
                result = pigpio._send_to_home_assistant({}, _TEST_CONFIG)  # pylint: disable=protected-access
        mock_post.assert_not_called()
        assert result is None

    def test_sends_if_domain_in_allowlist(self):
        """Vérifie que la requête est envoyée si le domaine est dans la whitelist."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        with patch.object(pigpio, "DOMAINS_ALLOWLIST", ["192.168.1.1"]):
            with patch("pigpio.requests.post", return_value=mock_response) as mock_post:
                result = pigpio._send_to_home_assistant({}, _TEST_CONFIG)  # pylint: disable=protected-access
        mock_post.assert_called_once()
        assert result == mock_response

    def test_returns_none_on_request_exception(self):
        """Vérifie que None est retourné en cas d'erreur réseau."""
        with patch.object(pigpio, "DOMAINS_ALLOWLIST", ["192.168.1.1"]):
            with patch(
                "pigpio.requests.post",
                side_effect=requests.exceptions.ConnectionError("err"),
            ):
                result = pigpio._send_to_home_assistant({}, _TEST_CONFIG)  # pylint: disable=protected-access
        assert result is None
