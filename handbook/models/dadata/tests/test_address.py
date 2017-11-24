# coding: utf-8

"""
Здесь будем проверять запросы к ресурсу типа адрес
"""
import json
import requests_mock

from .common import CommonTestCase
from dadata import DaDataClient

ADDRESS_REQUEST = "мск сухонска 11/-89"

ADDRESS_RESPONSE = """[
    {
    "source": "мск сухонска 11/-89",
    "result": "г Москва, ул Сухонская, д 11, кв 89",
    "postal_code": "127642",
    "country": "Россия",
    "region_fias_id": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
    "region_kladr_id": "7700000000000",
    "region_with_type": "г Москва",
    "region_type": "г",
    "region_type_full": "город",
    "region": "Москва",
    "area_fias_id": null,
    "area_kladr_id": null,
    "area_with_type": null,
    "area_type": null,
    "area_type_full": null,
    "area": null,
    "city_fias_id": null,
    "city_kladr_id": null,
    "city_with_type": null,
    "city_type": null,
    "city_type_full": null,
    "city": null,
    "city_area": "Северо-восточный",
    "city_district_fias_id": null,
    "city_district_kladr_id": null,
    "city_district_with_type": "р-н Северное Медведково",
    "city_district_type": "р-н",
    "city_district_type_full": "район",
    "city_district": "Северное Медведково",
    "settlement_fias_id": null,
    "settlement_kladr_id": null,
    "settlement_with_type": null,
    "settlement_type": null,
    "settlement_type_full": null,
    "settlement": null,
    "street_fias_id": "95dbf7fb-0dd4-4a04-8100-4f6c847564b5",
    "street_kladr_id": "77000000000283600",
    "street_with_type": "ул Сухонская",
    "street_type": "ул",
    "street_type_full": "улица",
    "street": "Сухонская",
    "house_fias_id": "5ee84ac0-eb9a-4b42-b814-2f5f7c27c255",
    "house_kladr_id": "7700000000028360004",
    "house_type": "д",
    "house_type_full": "дом",
    "house": "11",
    "block_type": null,
    "block_type_full": null,
    "block": null,
    "flat_type": "кв",
    "flat_type_full": "квартира",
    "flat": "89",
    "flat_area": "34.6",
    "square_meter_price": "198113",
    "flat_price": "6854710",
    "postal_box": null,
    "fias_id": "5ee84ac0-eb9a-4b42-b814-2f5f7c27c255",
    "fias_level": "8",
    "kladr_id": "7700000000028360004",
    "capital_marker": "0",
    "okato": "45280583000",
    "oktmo": "45362000",
    "tax_office": "7715",
    "tax_office_legal": null,
    "timezone": "UTC+3",
    "geo_lat": "55.8785292",
    "geo_lon": "37.6536442",
    "beltway_hit": "IN_MKAD",
    "beltway_distance": null,
    "qc_geo": 0,
    "qc_complete": 0,
    "qc_house": 2,
    "qc": 0,
    "unparsed_parts": null
}]"""


class AddressRequestTest(CommonTestCase):
    def setUp(self):
        self.client = DaDataClient(
            url="mock://api/v2",
            key="key",
            secret="secret",
        )
        adapter = requests_mock.Adapter()
        adapter.register_uri('POST',
                             'mock://api/v2/clean/address',
                             request_headers={'Authorization': 'Token key', 'X-Secret':'secret'},
                             text=ADDRESS_RESPONSE)
        self.client.session.mount('mock', adapter)

    def test_address_request(self):
        self.client.address = ADDRESS_REQUEST
        code = self.client.address.request()
        self.assertEqual(code, 200)
        result = self.client.result
        self.assertEqual(result.region_kladr_id, "7700000000000")
