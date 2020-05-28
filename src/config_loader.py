import os
import re
from ruamel import yaml
import logging


def overwrite_yml(cfg):
    with open("trad_config.yml", 'w') as yaml_file:
        yaml_file.write(yaml.round_trip_dump(cfg, default_flow_style=False, allow_unicode=True))


def load_yml():
    """Parse the YAML config"""
    pattern = re.compile(r"\$\{(.*)\}(.*)$")
    yaml.add_implicit_resolver("!env", pattern)

    def env_constructor(loader, node):
        """Constructor for environment variables"""
        value = loader.construct_scalar(node)
        env_var, remaining_path = pattern.match(value).groups()
        return os.environ[env_var] + remaining_path

    yaml.add_constructor('!env', env_constructor)
    with open("trad_config.yml") as config:
        try:
            cfg = yaml.load(config, Loader=yaml.Loader)
        except yaml.YAMLError:
            logging.error("Error while loading config file.")
            raise
    return cfg


class ConfigLoader:
    def __init__(self):
        self._cfg = value
        self._metadata = value

    @property
    def cfg(self):
        return self._cfg

    @cfg.setter
    def cfg(self, value):
        pass

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        pass
