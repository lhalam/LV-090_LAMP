"""This module implements common functions for interaction with ip address
database, it's a wrapper around MySQLdb and also uses netaddr module for
some operations on ip addresses."""
import MySQLdb as mdb

from config_parser import get_section_settings
from logging_conf import create_logger
from dbapi_exceptions import ConnectionError

MODULE_LOGGER = create_logger('logging.cfg', 'connector')


def get_database_connection(config, section):
    """Return database connection object.

    :param config: a path to database config file
    :returns: Returns a MYSQL connection object.

    """
    section_data = get_section_settings(config, section)
    try:
        connection = mdb.connect(
            host=section_data['host'],
            user=section_data['user'],
            passwd=section_data['password'],
            db=section_data['database_name'],
            port=int(section_data['port'])
        )
        connection.autocommit(1)
        MODULE_LOGGER.debug(
            "Connected. host - %s, database - %s"
            % (section_data['host'], section_data['database_name'])
        )
        return connection
    except mdb.OperationalError as connection_error:
        MODULE_LOGGER.error(connection_error.message)
        raise ConnectionError
