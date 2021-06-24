"""
config.py
"""
import pathlib as p
import yaml


def get_config(filename):
    """
    The method to get config settings from the example_config.yaml
    :param filename:
    :return: config
    """
    with p.Path(filename).open("r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config
