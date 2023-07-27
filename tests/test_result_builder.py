import unittest
import json
from custom_parser.result_builder import ResultBuilder
from custom_parser.mapping_provider import MappingProvider
from pathlib import Path


class TestResultBuilder(unittest.TestCase):

    BASE_PATH = Path(__file__).parent

    def setUp(self):
        self.mappings_file_path = (self.BASE_PATH / "data/sample_mappings.csv").resolve()
        self.pricat_file_path = (self.BASE_PATH / "data/sample_pricat.csv").resolve()
        self.mapping_provider = MappingProvider(self.mappings_file_path)
        self.result_builder = ResultBuilder(
            self.pricat_file_path, self.mapping_provider)
       
    def test_catalog_after_make_result(self):
        self.result_builder.make_result()

        self.assertEqual(self.result_builder.catalog.target_area, "Woman Shoes")
        self.assertEqual(len(self.result_builder.catalog.articles), 2)

        # article 1 must have 2 variations and 2 must have 4 variations
        self.assertEqual(len(self.result_builder.catalog.articles[0].variations), 2)
        self.assertEqual(len(self.result_builder.catalog.articles[1].variations), 4)

        # article 2 must have article_structure Boot
        self.assertEqual(self.result_builder.catalog.articles[1].article_structure, "Boot")

    def test_process_row(self):

        row = {'ean': '8719245200978', 'supplier': 'Rupesco BV', 'brand': 'Via Vai', 'catalog_code': '', 'collection': 'NW 17-18', 'season': 'winter', 'article_structure_code': '10', 'article_number': '15189-02', 'article_number_2': '15189-02 Aviation Nero',
               'article_number_3': 'Aviation', 'color_code': '1', 'size_group_code': 'EU', 'size_code': '38', 'size_name': '38', 'currency': 'EUR', 'price_buy_gross': '', 'price_buy_net': '58.5', 'discount_rate': '', 'price_sell': '139.95', 'material': 'Aviation', 'target_area': 'Woman Shoes'}
        processed_row = self.result_builder._process_row(row)

        self.assertEqual(processed_row['color'], "Nero")
        self.assertEqual(processed_row['article_number_3'], "Aviation")
