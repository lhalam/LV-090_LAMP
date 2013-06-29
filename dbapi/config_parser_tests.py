import unittest

from config_parser import get_section_settings
from dbapi_exceptions import ConfigError


class TestConfigParsing(unittest.TestCase):

    def setUp(self):
        self.config_file = 'test_config.cfg'
        self.section = "MySQL settings"

    def test_mysql_section_parameters(self):
        parameters = ('host', 'user', 'password', 'database_name', 'port')
        for parameter in get_section_settings(self.config_file, self.section):
            self.assertIn(parameter, parameters)

    def test_mysql_section_parameter_values(self):
        mysql_section_data = get_section_settings(
            self.config_file,
            self.section
        )
        self.assertEquals(mysql_section_data['host'], 'localhost')
        self.assertEquals(mysql_section_data['user'], 'root')
        self.assertEquals(mysql_section_data['password'], 'root')
        self.assertEquals(mysql_section_data['port'], '3306')

    def test_logging_section_parameters(self):
        parameters = ('file_level', 'logfile', 'console_level')
        for parameter in get_section_settings(self.config_file, 'Logging'):
            self.assertIn(parameter, parameters)

    def test_logging_section_parameters_values(self):
        logging_data = get_section_settings(self.config_file, 'Logging')
        self.assertEquals(logging_data['file_level'], 'debug')
        self.assertEquals(logging_data['console_level'], 'error')
        self.assertEquals(logging_data['logfile'], 'dbapi.log')


class TestConfigExceptions(unittest.TestCase):

    def test_ecxception_for_wrong_section(self):
        self.assertRaises(
            ConfigError,
            lambda: get_section_settings('test_config.cfg', 'SpamHam')
        )

    def test_ecxception_unexisting_config(self):
        self.assertRaises(
            ConfigError,
            lambda: get_section_settings('spamham.cfg', 'Logging')
        )

if __name__ == '__main__':
    unittest.main()
