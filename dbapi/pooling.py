import sqlalchemy.pool as pool

from mysql_connector import get_database_connection
from config_parser import get_section_settings


def create_pool(config):
    """Create a pool of database connections

    :param config: String with name of configuration file which contains
    connection settings.

    """
    pool_settings = get_section_settings(config, 'Pooling')
    mysql_pool = pool.QueuePool(
        lambda: get_database_connection(config, 'MySQL settings'),
        pool_size=int(pool_settings['pool_size']),
        max_overflow=int(pool_settings['max_overflow']),
        timeout=int(pool_settings['timeout']),
        recycle=int(pool_settings['recycle'])
    )
    return mysql_pool
