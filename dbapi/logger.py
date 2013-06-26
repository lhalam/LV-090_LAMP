import logging

from config_parser import get_section_settings

LOGGING_SECTION_NAME = 'Logging'


def create_logger(name, config):
    """Create and return logger object using settings from config file.

    :param name: name of some program unit (module, function, class etc.), for
    which events are logged. Expected type is string.
    :param config: a name or absolute path to config file where logger settings
    are stored. Config section that corresponds to logger can be modified in
    LOGGING_SECTION_NAME variable. Functions assumes that section contains
    'console_level' and 'file_level' options.

    """
    # get dictationary of config options for logger module
    config_data = get_section_settings(config, LOGGING_SECTION_NAME)
    # Convert them to uppercase for accurate usage with __getattribute__
    console_level_name = config_data['console_level'].upper()
    file_level_name = config_data['file_level'].upper()
    # get logging level for console and file
    # and set it to corresponding attribute
    console_level = logging.__getattribute__(console_level_name)
    file_level = logging.__getattribute__(file_level_name)
    # retrieve log file name
    logfile = config_data['logfile']

    # make nice formatting string
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logger = logging.getLogger(name)
    logger.setLevel(file_level)

    # Create file handler and set it's level
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(file_level)

    # Create console handler and set it's level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # Create formatter and assign it to file and console handlers
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add both handlers to logger object
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
