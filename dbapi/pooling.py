import sqlalchemy.pool as pool

from mysql_connector import get_database_connection

def create_pool(config, section, overflow, size):
    """Create a pool of database connections

    :param config: String with name of configuration file which contains
    connection settings.
    :param section: Config section with mysql settings.
    :param overflow: Maximum overflow size of the pool.
    :param size: Largest number of connections that will be kept persistently
    in the pool.

    """
    get_connection = lambda: get_database_connection(config, section)
    mysql_pool = pool.QueuePool(
        get_connection,
        max_overflow=overflow,
        pool_size=size
    )
    return mysql_pool

if __name__ == '__main__':
    my_pool = create_pool('test_config.cfg', 'MySQL settings', 10, 5)
    connection = my_pool.connect()
    cursor = connection.cursor()
    cursor.execute('select * from sources;')
    data = cursor.fetchall()
    connection.close()
