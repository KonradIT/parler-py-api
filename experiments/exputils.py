import csv
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from Parler import utils

def writetocsv(file, iterable, insert_headers=None):
    wroteheader = False
    for item in iterable:
        if not wroteheader and insert_headers is not None and insert_headers:
            fieldnames = item.keys()
            writer = csv.DictWriter(
                file, fieldnames=fieldnames, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
            writer.writeheader()
            wroteheader = True
        fieldnames = item.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames,
                                delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
        for k, v in item.items():
           
            if isinstance(v, str):
                item[k] = v.replace("\n", "\\n")
            else:
                item[k] = v
        writer.writerow(utils.add_missing_values(item))
