import unittest
from custom_parser.mapping_provider import MappingProvider


class TestMappingProvider(unittest.TestCase):

    def setUp(self) -> None:
        mappings_file_path = "/home/vinpalace/FCService/data/sample_mappings.csv"
        self.sample_mapping_provider = MappingProvider(mappings_file_path)

    def test_create_mapping_dicts(self):
        expected_destination_type_to_value_mapping = {'season': {'source_type': 'season', 'value_mappings': {'winter': 'Winter', 'summer': 'Summer'}}, 'collection': {'source_type': 'collection', 'value_mappings': {'NW 17-18': 'Winter Collection 2017/2018'}}, 'size': {'source_type': 'size_group_code|size_code', 'value_mappings': {'EU|36': 'European size 36', 'EU|37': 'European size 37', 'EU|38': 'European size 38', 'EU|39': 'European size 39', 'EU|40': 'European size 40', 'EU|41': 'European size 41', 'EU|42': 'European size 42'}}, 'article_structure': {'source_type': 'article_structure_code', 'value_mappings': {'4': 'Boot', '5': 'Sneaker', '6': 'Slipper', '7': 'Loafer', '8': 'Mocassin', '9': 'Sandal', '10': 'Pump'}}, 'color': {'source_type': 'color_code', 'value_mappings': {'1': 'Nero', '2': 'Marrone', '3': 'Brandy Nero', '4': 'Indaco Nero', '5': 'Fucile', '6': 'Bosco Nero'}}}
        expected_supported_keys = {'size_group_code', 'color_code', 'season', 'size_code', 'article_structure_code', 'collection'}

        self.assertDictEqual(self.sample_mapping_provider.destinationTypeToValueMapping,
                             expected_destination_type_to_value_mapping)
        self.assertEqual(self.sample_mapping_provider.supportedKeys,
                         expected_supported_keys)

    def test_get_value(self):
        key = "size"
        row = {'ean': '8719245200978', 'supplier': 'Rupesco BV', 'brand': 'Via Vai', 'catalog_code': '', 'collection': 'NW 17-18', 'season': 'winter', 'article_structure_code': '10', 'article_number': '15189-02', 'article_number_2': '15189-02 Aviation Nero', 'article_number_3': 'Aviation', 'color_code': '1', 'size_group_code': 'EU', 'size_code': '36', 'size_name': '36', 'currency': 'EUR', 'price_buy_gross': '', 'price_buy_net': '58.5', 'discount_rate': '', 'price_sell': '139.95', 'material': 'Aviation', 'target_area': 'Woman Shoes'}
        result = {'source_type': 'size_group_code|size_code', 'value_mappings': {'EU|36': 'European size 36'}}

        result = self.sample_mapping_provider.getValue(key, row)

        self.assertEqual(result, "European size 36")
