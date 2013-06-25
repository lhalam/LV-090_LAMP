"""Module for parsing config files using ConfigParser from standart library,
:functions: get_config_settings"""
import ConfigParser

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
    for option in config.options(section):
        # add each option of a section as value of dictationary
        section_dict[option] = config.get(section, option)
    return section_dict
