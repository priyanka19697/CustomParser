import json
from ..mapping_provider import MappingProvider
from collections import defaultdict
import csv

class Variation:
    def __init__(self) -> None:
        return
    
    def __str__(self):
        return str(self.__dict__)

class Article:
    def __init__(self, article_number) -> None:
        self.article_number = article_number
        self.variations = []
    
    def __str__(self):
        return str(self.__dict__)

class Catalog:
    def __init__(self) -> None:
        self.articles = []
        
    def __str__(self):
        return str(self.__dict__)

class ResultBuilder:
    def __init__(self, input_file, mapping_provider: MappingProvider) -> None:
        self.catalog = Catalog()
        self.mapping_provider = mapping_provider
        self._create_initial_articles(input_file)

    def process_row(self, row):
        new_row = {}
        supported_keys = self.mapping_provider.getSupportedKeys()
        available_destination_keys = self.mapping_provider.getAvailableDestinationKeys()
        for k, v in row.items():
            if k in supported_keys:
                continue
            else:
                new_row[k] = v

            for available_key in available_destination_keys:
                new_row[available_key] = self.mapping_provider.getValue(available_key, row)
        return new_row
    
    def _create_initial_articles(self, input_file):
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            # process each row
            articles_dict = defaultdict(list)
            for row in reader:
                articles_dict[row['article_number']].append(self.process_row(row=row))
            
            articles = []
            for article_number, article_variations in articles_dict.items():
                art = Article(article_number=article_number)
                variations = []
                for variation in article_variations:
                    var = Variation()
                    for k, v in variation.items():
                        setattr(var, k, v)
                    variations.append(var)
                art.variations = variations
                articles.append(art)

            self.catalog.articles = articles

    def make_result(self):
        json_data = json.dumps(self.catalog,  default=lambda o: o.__dict__)
        with open('data/result.json', 'w') as json_file:
            json_file.write(json_data)