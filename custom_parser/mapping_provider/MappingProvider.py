import csv
from operator import itemgetter

class MappingProvider:

    # takes mapping.csv and returns dicts for
    DELIMETER = "|"

    def __init__(self, mapping_file_path) -> None:
        self.destinationTypeToValueMapping = {}
        self.supportedKeys = set()
        self._createMappingDicts(mapping_file_path)

    def _createMappingDicts(self, file_path):
        DESTINATION_TYPE_COLUMN = 'destination_type'
        SOURCE_TYPE_COLUMN = 'source_type'
        try:
            with open(file_path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")

                for row in reader:
                    self.supportedKeys.update(row[SOURCE_TYPE_COLUMN].split(self.DELIMETER))
                    if row[DESTINATION_TYPE_COLUMN] not in self.destinationTypeToValueMapping:
                        self.destinationTypeToValueMapping[row[DESTINATION_TYPE_COLUMN]] = {
                            "source_type":  row[SOURCE_TYPE_COLUMN],
                            "value_mappings": {
                                row['source']: row['destination']
                            }
                    }
                    else:
                        self.destinationTypeToValueMapping[row[DESTINATION_TYPE_COLUMN]
                                                                ]["value_mappings"][row['source']] = row['destination']
                        
        except FileNotFoundError:
            print("File could not be found")

    def getSupportedKeys(self):
        return self.supportedKeys
    
    def getAvailableDestinationKeys(self):
        return set(self.destinationTypeToValueMapping.keys())

    def getSourceTypeForDestinationKey(self, destinationKey) -> list:
        try:
            return self.destinationTypeToValueMapping.get(destinationKey)
        except KeyError as e:
            raise KeyError(e) # TODO: Replace with custom error

    def getValue(self, destinationKey: str, row: dict):
        
        result = self.destinationTypeToValueMapping[destinationKey]
        source_type, value_mappings = itemgetter('source_type', 'value_mappings')(result)

        source_key_list = source_type.split(self.DELIMETER)
        value_mappings_key = self.DELIMETER.join([row[key] for key in source_key_list])

        return value_mappings[value_mappings_key]
