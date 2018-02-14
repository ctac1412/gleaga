import unittest
from dadata import DaDataclient


class CommonTestCase(unittest.TestCase):
    def setUp(self):
        self.client = DaDataclient()
        self.client_with_key = DaDataclient(key="anykey")
        self.client_with_key_secret = DaDataclient(key="anykey", secret="anysec")
