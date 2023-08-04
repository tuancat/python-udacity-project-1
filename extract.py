"""Extract data on near-Earth objects and close approaches
    from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.
The main module calls these functions
with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """_summary_

    Args:
        neo_csv_path (_type_): _description_

    Returns:
        _type_: _description_
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
    """_summary_

    Args:
        cad_json_path (_type_): _description_

    Returns:
        _type_: _description_
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
    """_summary_
    """
    load_neos("data/neos.csv")
    # load_approaches('data/cad.json')


if __name__ == "__main__":
    main()
