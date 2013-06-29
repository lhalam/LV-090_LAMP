import unittest
from pooling import create_pool


class PoolingTest(unittest.TestCase):

    def setUp(self):
        self.pool = create_pool('dbapi.cfg', 'MySQL settings', 10, 5)

    def tearDown(self):
        self.pool = self.pool.recreate()

    def test_empty_pool(self):
        self.assertEquals(self.pool.overflow(), -5)

    def test_creating_connecton(self):
        self.pool.connect()
        self.assertEquals(self.pool.overflow(), -4)
        self.assertEquals(self.pool.checkedin(), 1)

    def test_creating_and_closing_connection(self):
        connection = self.pool.connect()
        connection.begin()
        self.assertEquals(self.pool.overflow(), -4)
        self.assertEquals(self.pool.checkedin(), 1)
        print self.pool.status()


if __name__ == '__main__':
    unittest.main()
