"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """_summary_.

    Args:
        neo_csv_path (_type_): _description_.

    Returns:
        _type_: _description_.
    """
    data = []
    with open(neo_csv_path, "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            neo = NearEarthObject(row[3], row[4], row[15], row[7])
            data.append(neo)
    return data


def load_approaches(cad_json_path):
    """_summary_.

    Args:
        cad_json_path (_type_): _description_.

    Returns:
        _type_: _description_.
    """
    # Extract data into Python
    data = []
    with open(cad_json_path, "r") as infile:
        # Parse JSON data into a Python object. (A)
        contents = json.load(infile)
        for row in contents["data"]:
            element = CloseApproach(row[0], row[3], row[4], row[7])
            data.append(element)

    return data


def main():
    """_summary_."""
    load_neos("data/neos.csv")
    # load_approaches('data/cad.json').


if __name__ == "__main__":
    main()
