import sys

from custom_parser.mapping_provider.MappingProvider import MappingProvider
from custom_parser.result_builder.ResultBuilder import ResultBuilder

if len(sys.argv) != 3:
    print("usage: python main.py <mapping_file_path> <pricat_file_path>")
    sys.exit(1)

mapping_file = sys.argv[1]
# mapping_file = "/home/vinpalace/FCService/data/mappings.csv"
pricat_file = sys.argv[2]
# pricat_file = "/home/vinpalace/FCService/data/pricat.csv"

mapping_provider = MappingProvider(mapping_file)
result_builder = ResultBuilder(pricat_file, mapping_provider)

result_builder.make_result()