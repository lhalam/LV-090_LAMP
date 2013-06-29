"""Module for parsing config files using ConfigParser from standart library,
:functions: get_config_settings"""
import ConfigParser
import os

from dbapi_exceptions import ConfigError


def get_section_settings(filename, section):
    """
    Parse config file and retrieve all config data from that file as a
    dicatationary.

    param: filename: Name of config file
    param: section:
    returns: Return a dicatationary with keys as configuration file sections
    and values as dicatationaries too, where key is a config parameter and
    value is corresponding config value
    raises:
    """
    config = ConfigParser.ConfigParser()
    config.read(filename)
    # Initialize empty config dictationary
    section_dict = dict()
    if (not config.has_section(section)) or (not os.path.exists(filename)):
        raise ConfigError
    for option in config.options(section):
        # add each option of a section as value of dictationary
        section_dict[option] = config.get(section, option)
    return section_dict
