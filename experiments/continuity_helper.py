from io import TextIOWrapper
from enum import Enum
import csv

class ItemType(Enum):
    POST = 0
    LINK = 1
    
"""
Utility to get last post/link/etc... id from a csv file
"""
def get_last_id(file: TextIOWrapper, item: ItemType) -> str:
	reader = csv.reader(file, delimiter=",", quotechar="\"")

	lastitem = None
	for row in reader:
		lastitem=row
	return lastitem["Id2"]