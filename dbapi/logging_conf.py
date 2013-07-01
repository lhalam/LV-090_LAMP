"""This module simply create loggers from config file. To configure new
look for examples in 'logging.cfg' file"""
import logging.config
import os
from ConfigParser import NoSectionError, NoOptionError

from dbapi_exceptions import ConfigError


def create_logger(config, logger_name):
    """Create logger object using options from config file"""
    if not os.path.exists(config):
        raise ConfigError
    try:
        logging.config.fileConfig(config)
    except (NoSectionError, NoOptionError):
        raise ConfigError
    try:
        return logging.getLogger(logger_name)
    except KeyError:
        raise Exception("There is no such logger in configuration file")
