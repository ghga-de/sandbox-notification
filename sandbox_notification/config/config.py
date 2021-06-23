"""
config.py
"""
import os.path
import yaml


def get_config(filename):
    """
    The method to get config settings from the example_config.yaml
    :param filename:
    :return: config
    """
    with open(os.path.relpath(filename), "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config
