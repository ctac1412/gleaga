# coding: utf-8
"""
Проверяем конфигурируемость клиента
"""
import unittest
from .common import CommonTestCase
from dadata import DaDataclient


class DefaultsTest(CommonTestCase):
    def test_url(self):
        self.assertEqual(self.client.url, self.client.url)

    def test_url_override(self):
        client = DaDataclient(url='http://myurl')
        self.assertEqual(client.url, 'http://myurl')
