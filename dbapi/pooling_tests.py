import unittest
from pooling import create_pool


class PoolingTest(unittest.TestCase):

    def setUp(self):
        self.pool = create_pool('dbapi.cfg')

    def tearDown(self):
        self.pool = self.pool.recreate()

    def test_empty_pool(self):
        self.assertEquals(self.pool.overflow(), -5)

    def test_creating_and_closing_connection(self):
        connection = self.pool.connect()
        self.assertEquals(self.pool.overflow(), -4)
        self.assertEquals(self.pool.checkedout(), 1)
        connection.close()
        self.assertEquals(self.pool.checkedin(), 1)
        self.assertEquals(self.pool.checkedout(), 0)


if __name__ == '__main__':
    unittest.main()
