import logging

from config_parser import get_section_settings

LOGGING_SECTION_NAME = 'Logging'


def create_logger(name, config):
    """Create logger object"""
    # get dictationary of config options for logger module
    config_data = get_section_settings(config, LOGGING_SECTION_NAME)
    level_name = config_data['level'].upper()
    # get logging level and set it to corresponding attribute
    level = logging.__getattribute__(level_name)
    logfile = config_data['logfile']

    # make nice formatting string
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
