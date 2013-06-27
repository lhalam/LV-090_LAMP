"""Module implements common queries at ip addresses database, each represented
as a function (for now), each function takes MySQLdb.Connection as a first
parameter, other parameter depend on function itself. Functions use MySQLdb
library for executing queries and retrieving data"""
from datetime import datetime

import MySQLdb as mdb
from netaddr import IPAddress

from logger import create_logger

MODULE_LOGGER = create_logger('dbapi', 'test_config.cfg')


def get_ip_data(ip_address):
    """Return value of ip address and ip version (value is integer if ip version
    is 4 and binary - if ip version is 6

    :param ip_address: ip address in string form.

    """
    ip = IPAddress(ip_address)
    ip_version = ip.version
    ip_value = ip.value if ip_version == 4 else bin(ip)
    return ip_value, ip_version

def add_sql_limit(sql, limit):
    """Add limit clause to sql query text

    :param sql: String containing sql query that should be limited
    :param limit: A tuple of integers for offset and row count in limit clause

    """
    # strip off trialing whitespaces, remove ";" from end and add limit
    sql_with_limit = sql.rstrip()[:-1] + ' LIMIT %s, %s;' % limit
    return sql_with_limit


def get_ip_with_source_name(connection, sourcename, limit=None):
    """Get all ip addresses (if limit is not set), whose source name match
    to specified in function argument, if limit is set - output is limited to
    according values

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param sourcename: The name of ip addresses source.
    :type sourcename: str.
    :param limit: A tuple of offset and row count.
    :type: limit: tuple.
    :returns: tuple -- each inner tuple contains all values from ip addresses
    table that match sourcename.

    """
    cursor = connection.cursor()
    sql = '''
    SELECT * FROM ip{0}_addresses
    WHERE id IN
    (
        SELECT source_to_addresses.{0}_id FROM source_to_addresses
        JOIN sources ON source_to_addresses.source_id = sources.id
        WHERE sources.source_name = "{1}"
    );'''
    if limit:
        sql = add_sql_limit(sql, limit)
    # create queries for v4 and v6 ip addresses
    sql_v4 = sql.format('v4', sourcename)
    sql_v6 = sql.format('v6', sourcename)
    # execute and fetch all results
    cursor.execute(sql_v4)
    result_v4 = cursor.fetchall()
    cursor.execute(sql_v6)
    result_v6 = cursor.fetchall()
    # close cursor and return all results
    result = result_v4 + result_v6
    cursor.close()
    MODULE_LOGGER.debug(
        'Searching for ips with source named "%s", found %s'
        % (sourcename, len(result))
    )
    return result


def get_ip_from_range(connection, start, end, limit=None):
    """Get all information about ip addresses in some range

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param start: Start ip-address.
    :type start: str.
    :param end: End ip-address.
    :type end: str.
    :param limit: A tuple of offset and row count.
    :type: limit: tuple.
    :returns: tuple -- each inner tuple contains all values from ip addresses
    table within range.

    """
    cursor = connection.cursor()
    sql = '''
    SELECT * FROM ipv{0}_addresses
    WHERE address BETWEEN {1} AND {2};'''
    if limit:
        # if "limit" parameter is set, add LIMIT clause to sql query
        sql = add_sql_limit(sql, limit)
    # check if ip versions match
    start_value, start_version = get_ip_data(start)
    end_value, end_version = get_ip_data(end)
    if start_version != end_version:
        raise Exception("Different ip versions in start and end")
    # format query according to ip version, start and end values
    sql = sql.format(start_version, start_value, end_value)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    MODULE_LOGGER.debug(
        'Searching for ips in range %s - %s, limit is %s, found %s'
        % (start, end, limit, len(result))
    )
    return result


def find_ip_list_type(connection, ip_address):
    """Find to which list ip address belongs

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param ip_address: ip-address.
    :type start: str.
    :returns: str -- list name 'whitelsit' or 'blacklist' if found, else None

    """
    cursor = connection.cursor()
    sql = '''
    SELECT count(*) FROM {0}
    WHERE v{1}_id_{0} =
    (
        SELECT id FROM ipv{1}_addresses
        WHERE address = {2}
    );
    '''
    ip_value, ip_version = get_ip_data(ip_address)
    # format sql for whitelist and blacklist
    sql_whitelist = sql.format('whitelist', ip_version, ip_value)
    sql_blacklist = sql.format('blacklist', ip_version, ip_value)
    cursor.execute(sql_whitelist)
    # get number of address occurrences
    whitelist_count = cursor.fetchone()[0]
    cursor.execute(sql_blacklist)
    blacklist_count = cursor.fetchone()[0]
    if whitelist_count == blacklist_count:
        if whitelist_count > 0:
            raise Exception("Ip both in white and black lists, something wrong")
        return None
    cursor.close()
    list_name = 'whitelist' if whitelist_count > 0 else 'blacklist'
    MODULE_LOGGER.debug("Get %s list type. Found: %s" % (ip_address, list_name))
    return list_name


def get_ips_added_in_range(connection, startdate, enddate, limit=None):
    """Get information about ip addresses added since startdate till enddate

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param startdate: Date range start.
    :type start: datetime.datetime.
    :param enddate: Date range end.
    :type enddate: datetime.datetime.
    :param limit: A tuple of offset and row count.
    :type: limit: tuple.
    :returns: tuple -- each inner tuple contains all values from ip addresses
    table within date range

    """
    if startdate > enddate:
        raise Exception("End date is before start date")
    sql = """
    SELECT * FROM ipv{0}_addresses
    WHERE date_added BETWEEN '{1}' AND '{2}';"""
    if limit:
        # if "limit" parameter is set, add LIMIT clause to sql query
        sql = add_sql_limit(sql, limit)
    # get formated date string
    cursor = connection.cursor()
    sql_v4 = sql.format(4, startdate.date(), enddate.date())
    cursor.execute(sql_v4)
    result_v4 = cursor.fetchall()
    sql_v6 = sql.format(6, startdate.date(), enddate.date())
    cursor.execute(sql_v6)
    result_v6 = cursor.fetchall()
    cursor.close()
    result = result_v4 + result_v6
    MODULE_LOGGER.debug(
        "Get ips added since %s till %s, limit is %s. Found: %s"
        % (startdate, enddate, limit, len(result))
    )
    return result_v4 + result_v6


def get_sources_modified_in_range(connection, startdate, enddate, limit=None):
    """Get information about sources modified since startdate till enddate

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param startdate: Date range start.
    :type start: datetime.datetime.
    :param enddate: Date range end.
    :type enddate: datetime.datetime.
    :param limit: A tuple of offset and row count.
    :type: limit: tuple.
    :returns: tuple -- each inner tuple contains all values from ip addresses
    table within date range

    """
    cursor = connection.cursor()
    sql = '''
    SELECT * FROM sources
    WHERE url_date_modified
    BETWEEN "{0}" AND "{1}";'''.format(startdate.date(), enddate.date())
    if limit:
        # if "limit" parameter is set, add LIMIT clause to sql query
        sql = add_sql_limit(sql, limit)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    MODULE_LOGGER.debug(
        "Get sources modified since %s till %s, limit is %s. Found: %s"
        % (startdate, enddate, limit, len(result))
    )
    return result


def check_if_ip_in_database(connection, ip_address):
    """Get information about sources modified since startdate till enddate

    :param connection: MySQL database connection.
    :type connection: MySQLdb.connections.Connection.
    :param ip_address: Ip address to check.
    :type ip_address: str.
    :returns: boolean -- True if ip in database, else False.

    """
    ip_value, ip_version = get_ip_data(ip_address)
    sql = '''
    SELECT count(id) FROM ipv{0}_addresses
    WHERE address = {1};
    '''.format(ip_version, ip_value)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    cursor.close()
    result = True if result else False
    MODULE_LOGGER.debug(
        'Check if %s is in database. Returned: %s'
        % (ip_address, result)
    )
    return result


'''delete function'''

def findID(connection, ip_address):
    '''Define the IP id
    :param connect: object connection to the database
    :type connect: object
    :param ip: ip address
    :type ip: str
    '''
    ipv = get_ip_data(ip_address)[1]
    ip_address = get_ip_data(ip_address)[0]
    sql = "SELECT id FROM ipv%s_addresses WHERE address = %s"%(ipv,ip_address)
    cursor = connection.cursor()
    try:
        # Execute the SQL command
        cursor.execute(sql)
        #Selects all data from a table
        ipid = cursor.fetchone()
        cursor.close()
        return ipid[0]
    except mdb.Error:
        logging.error('Failed to find IP id')


def delIpFromList(connection, ip_address, lists):
    '''Removes the IP from black or white list
    :param connect: object connection to the database
    :type connect: object
    :param ip: ip address
    :type ip: str
    :param lists: black or white list
    :type lists: string (blacklist or whitelist)
    :raises: AttributeError, TypeError
    '''
    ipid = findID(connection, ip_address)
    #Version detection
    ipv = get_ip_data(ip_address)[1]
    sql = "DELETE FROM %s WHERE v%s_id_%s = %s"%(lists,ipv,lists,ipid)
    cursor = connection.cursor()
    try:
        #Execute the SQL command
        cursor.execute(sql)
        cursor.close()
    except mdb.Error:
        # Rollback in case there is any error
        connection.rollback()
        logging.error('Failed to remove IP from the lists')
        

def deleteIp(connection, ip_address):
    '''Removes the IP from database
    :param connect: object connection to the database
    :type connect: object
    :param ip: ip address
    :type ip: ip
    '''
    #Version detection
    ipid = findID(connection, ip_address)
    ipv = get_ip_data(ip_address)[1]
    ip_address = get_ip_data(ip_address)[0]
    sql = "DELETE FROM `ipv%s_addresses` WHERE `address` = %s"%(ipv,ip_address)
    sql1 = "DELETE FROM `blacklist` WHERE `v%s_id_blacklist` = %s"%(ipv,ipid)
    sql2 = "DELETE FROM `whitelist` WHERE `v%s_id_whitelist` = %s"%(ipv,ipid)
    sql3 = "DELETE FROM `source_to_addresses` WHERE `v%s_id` = %s"%(ipv,ipid)
    try:
        #Execute the SQL command
        cursor = connection.cursor()
        cursor.execute(sql3)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql)
    except mdb.Error:
        # Rollback in case there is any error
        connection.rollback()
        logging.error('Failed to remove IP from the database')

def deleteIpRange(connection, ip1, ip2):
    '''Remove IP from the range
    :param connect: object connection to the database
    :type connect: object
    :param ip1: starting ip address
    :type ip1: ip
    :param ip2: end ip address
    :type ip2: ip

    '''
    ipv = get_ip_data(ip_address)[1]
    ip1 = get_ip_data(ip1)[0]
    ip2 = get_ip_data(ip2)[0]
    
    sql = 'SELECT `id` FROM `ipv%s_addresses` WHERE `address`BETWEEN %s AND %s'%(ipv,ip1,ip2)
    sqldel = 'DELETE FROM `ipv%s_addresses` WHERE `address` BETWEEN %s AND %s'%(ipv,ip1,ip2)
    try:
        cursor = connection.cursor()
        #Execute the SQL command
        cursor.execute(sql)
        #Commit your changes in the database
        fetch = cursor.fetchall()
        for x in fetch:
            if ipv == 4:
                lists = 'DELETE FROM `source_to_addresses` WHERE `v4_id` = %s'%(x)
                cursor.execute(lists)
                lists1 = 'DELETE FROM `blacklist` WHERE `v4_id_blacklist` = %s'%(x)
                cursor.execute(lists1)
                lists2 = 'DELETE FROM `whitelist` WHERE `v4_id_whitelist` = %s'%(x)
                cursor.execute(lists2)
            else:
                lists = 'DELETE FROM `source_to_addresses` WHERE `v6_id` = %s'%(x)
                cursor.execute(lists)
                lists1 = 'DELETE FROM `blacklist` WHERE `v6_id_blacklist` = %s'%(x)
                cursor.execute(lists1)
                lists2 = 'DELETE FROM `whitelist` WHERE `v6_id_whitelist` = %s'%(x)
                cursor.execute(lists2)
        #Execute the SQL command
        cursor.execute(sqldel)
    except mdb.Error:
        # Rollback in case there is any error
        connection.rollback()
        logging.error('Failed to remove range IP from the database')

def get_ip_not_in_source (connection, limit=None):
    """Select all IP without sources

    :param connection: connections data
    :type connection: class 'MySQLdb.connections.Connection'
    :param limit: A tuple of offset and row count.
    :type: limit: tuple.
    :returns: tuple -- tuple that contains all info from ip tables,
    where IP without sourcename.
    """
    cursor = connection.cursor()
    sql = """
    SELECT * FROM ip{0}_addresses 
    WHERE id NOT IN 
    (
    SELECT {0}_id FROM source_to_addresses
    );"""
    if limit:
        sql = add_sql_limit(sql, limit)
    sql_v4 = sql.format('v4')
    sql_v6 = sql.format('v6')
    cursor.execute(sql_v4)
    result_v4 = cursor.fetchall()
    cursor.execute(sql_v6)
    result_v6 = cursor.fetchall()
    result = result_v4 + result_v6
    cursor.close()
    MODULE_LOGGER.debug(
        'Searching for ips without source, found %s'
        % (len(result))
    )
    return result
def get_source_by_sourcename (connection,sourcename):
    """Search source by name and return whole information
    about it from table 'sources'

    :param connection: connections data.
    :type connection: class 'MySQLdb.connections.Connection'.
    :param sourcename: selected source.
    :type sourcename: str.
    :returns: tuple -- tuple contains all values from table 'sources'
    if selected sourcename exist.
    """
    cursor = connection.cursor()
    sql = """
    SELECT * FROM sources 
    WHERE `source_name` =  '%s' """ %sourcename
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    except mdb.Error:
        logging.error('Entered sourcename not exist')