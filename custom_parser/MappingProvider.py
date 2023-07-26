import csv

class MappingProvider:

# takes mapping.csv and returns dicts for 
    DELIMETER = "|"

    def __init__(self, mapping_file) -> None:
        self.sourceValueToDestinationValueMapping = {}
        self.destinationTypeToSourceTypeMapping = {}
        self.mapping_file = mapping_file
    
    def _createMappingDicts(self):
       
        try:
            with open(self.mapping_file) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                
                for row in reader:
                    if row['destination_type'] not in self.destinationTypeToSourceTypeMapping:
                        self.destinationTypeToSourceTypeMapping[row['destination_type']] = row['source_type']
                    
                    self.sourceValueToDestinationValueMapping[row['source']] = row['destination']
                    
        except FileNotFoundError:
            print("File could not be found")

        
    def getMappingForDestinationType(self, json_key):
        # takes in size and gives size_group_code|size_code
        result_columns = self.destinationTypeToSourceTypeMapping[json_key]
        return result_columns.split(self.DELIMETER) # [size_group_code, size]

    def getValueForSource(self, *columnValues): # [EU, 42]
        key = self.DELIMETER.join(columnValues)
        return self.sourceValueToDestinationValueMapping[key] # European size 42






    





