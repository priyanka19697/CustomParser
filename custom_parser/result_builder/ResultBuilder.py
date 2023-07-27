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
                # import pdb;pdb.set_trace()
                new_row[available_key] = self.mapping_provider.getValue(
                    available_key, row
                )
        return new_row

    def make_result(self):
        self.bubble_up()
        return json.dumps(self.catalog, default=lambda o: o.__dict__)

    def _create_initial_articles(self, input_file):
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            # process each row
            articles_dict = defaultdict(list)
            for row in reader:
                articles_dict[row["article_number"]].append(self.process_row(row=row))

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

    def _find_common_attributes(self, objects: list) -> list:
        # Takes in list of objects of same type, then returns
        # list of attributes that were common across all the objects

        # Parameters:
        #   objects (list): list of objects

        # Returns
        #   list: list of attribute keys as strings
        common_attributes = []
        result = defaultdict(set)
        for obj in objects:
            for k, v in obj.__dict__.items():
                # skip complex types
                if type(v) == list:
                    continue
                result[k].add(v)

        for attr, value_list in result.items():
            if len(value_list) == 1:
                common_attributes.append(attr)

        return common_attributes

    def _find_common_attributes2(self, objects: list) -> list:
        # Takes in list of objects of same type, then returns
        # list of attributes that were common across all the objects

        # Parameters:
        #   objects (list): list of objects

        # Returns
        #   list: list of attribute keys as strings
        reference = objects[0]
        attributes = reference.__dict__

        common_attrs = []
        for k, v in attributes.items():
            flag = True
            for obj in objects:
                if getattr(obj, k) != v:
                    flag = False
            if flag:
                common_attrs.append(k)

        return common_attrs

    def _bubble_up_common_to_parent(self, parent_obj, nested_objects):
        # Takes in an object and a list of objects. From this list
        # of objects it finds attributes which have common values
        # (have same value in all the objects) then puts it in parent_obj
        # and removes from nested objects
        # NOTE: This mutates the parent object and nested_objects

        # Parameters:
        #   parent_obj: object
        #   nested_objects: list of objects

        # Returns
        #   None

        common_attributes = self._find_common_attributes2(nested_objects)

        reference_obj = nested_objects[0]  # just to get values to bubble up

        for attr in common_attributes:
            setattr(parent_obj, attr, getattr(reference_obj, attr, None))  # move

        for nested_obj in nested_objects:
            for attr in common_attributes:
                delattr(nested_obj, attr)  # delete from child objects

    def bubble_up(self):
        for article in self.catalog.articles:
            self._bubble_up_common_to_parent(article, article.variations)

        self._bubble_up_common_to_parent(self.catalog, self.catalog.articles)