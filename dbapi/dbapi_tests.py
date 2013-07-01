import unittest
from datetime import datetime

from netaddr import IPAddress

import dbapi
from mysql_connector import get_database_connection
from dbapi_exceptions import IPAddressError, SQLSyntaxError


class TestDBAPI(unittest.TestCase):

    def setUp(self):
        self.connection = get_database_connection('dbapi.cfg',
                                                  'MySQL settings')

    def test_get_ip_data(self):
        self.assertEquals(dbapi.get_ip_data('192.168.1.15'), (3232235791, 4))
        self.assertEquals(
            dbapi.get_ip_data('fe80::200:5aee:feaa:20a2'),
            (bin(IPAddress('fe80::200:5aee:feaa:20a2')), 6)
        )

    def test_wrong_ip_format(self):
        self.assertRaises(
            IPAddressError,
            dbapi.get_ip_data,
            'SpamHam'
        )

    def test_add_sql_limit(self):
        self.assertEqual(
            'SELECT * FROM spam LIMIT 5, 10;',
            dbapi.add_sql_limit('SELECT * FROM spam;', (5, 10))
        )
        self.assertEqual(
            'SELECT * FROM spam LIMIT 5, 10;',
            dbapi.add_sql_limit('SELECT * FROM spam', (5, 10))
        )

    def test_get_ip_with_source_name(self):
        ips = dbapi.get_ip_with_source_name(self.connection, 'test2')
        self.assertEquals(ips[0][1], 3232235777L)
        self.assertEquals(ips[1][1], 3232235791L)
        self.assertEquals(len(ips), 2)

    def test_get_ip_with_source_name_and_limit(self):
        ips = dbapi.get_ip_with_source_name(self.connection, 'test2', (0, 1))
        self.assertEquals(ips[0][1], 3232235777L)
        self.assertEquals(len(ips), 1)

    def test_get_ip_with_source_name_error(self):
        self.assertRaises(
            SQLSyntaxError,
            dbapi.get_ip_with_source_name,
            self.connection,
            'SpamHam',
            (0, -50)
        )

    def test_empty_get_ip_with_source_name(self):
        ips = dbapi.get_ip_with_source_name(self.connection, 'spam ham')
        self.assertFalse(ips)

    def test_get_ip_from_range(self):
        ips = dbapi.get_ip_from_range(
            self.connection,
            '192.168.1.1',
            '192.168.1.15'
        )
        self.assertEquals(ips[0][1], 3232235777L)
        self.assertEquals(ips[1][1], 3232235791L)
        self.assertEquals(len(ips), 2)

    def test_get_ip_from_range_with_limit(self):
        ips = dbapi.get_ip_from_range(
            self.connection,
            '192.168.1.1',
            '192.168.1.15',
            (0, 1)
        )
        self.assertEquals(ips[0][1], 3232235777L)
        self.assertEquals(len(ips), 1)

    def test_get_ip_from_wrong_range(self):
        self.assertRaises(
            Exception,
            dbapi.get_ip_from_range,
            self.connection,
            '192.168.161.22',
            '::1'
        )

    def test_get_ip_from_range_error(self):
        self.assertRaises(
            SQLSyntaxError,
            dbapi.get_ip_from_range,
            self.connection,
            '192.168.161.22',
            '192.168.161.55',
            (0, -1)
        )

    def test_find_ip_list_type(self):
        self.assertEquals(
            dbapi.find_ip_list_type(self.connection, '192.168.1.1'),
            'whitelist'
        )
        self.assertEquals(dbapi.find_ip_list_type(
            self.connection, '1.1.1.1'),
            'blacklist'
        )
        self.assertIsNone(dbapi.find_ip_list_type(
            self.connection,
            '192.112.121.12')
        )

    def test_get_ips_added_in_range(self):
        addresses = dbapi.get_ips_added_in_range(
            self.connection,
            datetime(1988, 06, 06),
            datetime.now()
        )
        self.assertEquals(len(addresses), 10)

    def test_get_ips_added_in_range_empty(self):
        addresses = dbapi.get_ips_added_in_range(
            self.connection,
            datetime(1988, 06, 06),
            datetime(1988, 06, 07)
        )
        self.assertEquals(len(addresses), 0)

    def test_get_ips_added_in_range_with_limit(self):
        addresses = dbapi.get_ips_added_in_range(
            self.connection,
            datetime(1988, 06, 06),
            datetime.now(),
            (0, 5)
        )
        self.assertEquals(len(addresses), 5)

    def test_get_ips_added_in_range_with_date_error(self):
        self.assertRaises(
            Exception,
            dbapi.get_ips_added_in_range,
            self.connection,
            datetime.now(),
            datetime(1988, 06, 06),
            (0, 5)
        )

    def test_get_sources_modified_in_range(self):
        self.assertEquals(
            len(
                dbapi.get_sources_modified_in_range(
                    self.connection,
                    datetime(1988, 06, 06),
                    datetime.now()
                )
            ),
            0
        )

    def test_get_sources_modified_in_range_with_limit(self):
        self.assertEqual(
            len(
                dbapi.get_sources_modified_in_range(
                    self.connection,
                    datetime.now(),
                    datetime.now(),
                    (0, 10)
                )
            ),
            0
        )

    def test_check_if_ip_in_database(self):
        self.assertTrue(
            dbapi.check_if_ip_in_database(self.connection, '192.168.1.15')
        )
        self.assertFalse(
            dbapi.check_if_ip_in_database(self.connection, '192.168.1.16')
        )

if __name__ == '__main__':
    unittest.main()
