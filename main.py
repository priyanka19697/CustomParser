import sys

from custom_parser.mapping_provider import MappingProvider
from custom_parser.result_builder import ResultBuilder

if len(sys.argv) != 3:
    print("usage: python main.py <mapping_file_path> <pricat_file_path>")
    sys.exit(1)

mapping_file = sys.argv[1]
pricat_file = sys.argv[2]

mapping_provider = MappingProvider(mapping_file)
result_builder = ResultBuilder(pricat_file, mapping_provider)

print(result_builder.make_result())