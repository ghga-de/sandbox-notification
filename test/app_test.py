"""
app_test.py
"""
from sandbox_notification.config import config


CONFIG_YAML = "../example_config.yaml"
HOST = 'host'


def test_config():
    """
    test case to test if the config file example_config.yaml is readable.
    :return:
    """
    config_data = config.get_config(CONFIG_YAML)
    assert config_data[HOST] == "0.0.0.0"
