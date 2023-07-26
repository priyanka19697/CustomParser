
from custom_parser.MappingProvider import MappingProvider
mappingProvider = MappingProvider("/home/vinpalace/FCService/data/mappings.csv")
# mappingProvider.read_mapping_file()


mappingProvider._createMappingDicts()
map1 = mappingProvider.destinationTypeToSourceTypeMapping
map2 = mappingProvider.sourceValueToDestinationValueMapping
print(map1)
print("----------------------------------------------")
print(map2)


modified_key = mappingProvider.getMappingForDestinationType("size")
print(modified_key)

modified_value = mappingProvider.getValueForSource("EU","36")
print(modified_value)

