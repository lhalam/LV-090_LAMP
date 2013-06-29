"""Module containing custom dbapi exceptions.
Possible MySQLdb exceptions: DataError, DatabaseError, IntegrityError,
InterfaceError, InternalError, MySQLError, NotSupportedError, OperationalError,
ProgrammingError.
"""


class ConnectionError(Exception):
    """Used in case of mdb.OperationalError"""
    def __init__(self):
        message = "Error connecting, check host, user, password or database " \
                  "name"
        Exception.__init__(self, message)


class ConfigError(Exception):
    """Used in case of ConfigParser's NoSectionError or NoOptionError or
    if there is no such config file"""
    def __init__(self):
        message = "Error parsing config file, check if file exist and it " \
                  "have correct section and section have correct options"
        Exception.__init__(self, message)


class SQLSyntaxError(Exception):
    """Used in case of MySQLdb.ProgrammingError."""
    def __init__(self):
        message = "Error in sql syntax"
        Exception.__init__(self, message)


class IPAddressError(Exception):
    """Used in case of netaddr.core.AddrFormatError"""
    def __init__(self):
        message = "IP address is not valid."
        Exception.__init__(self, message)
