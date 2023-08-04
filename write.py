"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from json import JSONEncoder
from datetime import datetime
from helpers import datetime_to_str


class DataEncoder(JSONEncoder):
    """_summary_.

    Args:
        JSONEncoder (_type_): _description_.
    """

    def default(self, o):
        """_summary_.

        Args:
            o (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        if isinstance(o, datetime):
            return datetime_to_str(o)
        else:
            return super().default(o)


class NearEarthObjectJSON:
    """_summary_."""

    def __init__(self, neo):
        """_summary_.

        Args:
            neo (_type_): _description_.
        """
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self.designation = neo.designation
        self.name = neo.name
        self.diameter_km = neo.diameter
        self.potentially_hazardous = neo.hazardous
        # self.neo = approach.neo

    def default(self, o):
        """_summary_.

        Args:
            o (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return o.__dict__


class CloseApproachJSON:
    """_summary_."""

    def __init__(self, approach, neoJson):
        """_summary_.

        Args:
            approach (_type_): _description_.
            neoJson (_type_): _description_.
        """
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self.datetime_utc = approach.time_str
        self.distance_au = approach.distance
        self.velocity_km_s = approach.velocity
        self.neo = neoJson.__dict__

    def default(self, o):
        """_summary_.

        Args:
            o (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return o.__dict__


def write_to_csv(results, filename):
    """_summary_.

    Args:
        results (_type_): _description_.
        filename (_type_): _description_.
    """
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for elem in results:
            row = {
                "datetime_utc": elem.time_str,
                "distance_au": elem.distance,
                "velocity_km_s": elem.velocity,
                "designation": elem._designation,
                "name": elem.neo.name,
                "diameter_km": elem.neo.diameter,
                "potentially_hazardous": elem.neo.hazardous,
            }
            writer.writerow(row)


def dumper(obj):
    """_summary_.

    Args:
        obj (_type_): _description_.

    Returns:
        _type_: _description_.
    """
    return obj.toJSON()

def write_to_json(results, filename):
    """_summary_.

    Args:
        results (_type_): _description_.
        filename (_type_): _description_.
    """
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    """
    # Write available listings to an output file.
    first_item = True
    with open(filename, "w") as outfile:
        outfile.write("[")
        for e in results:
            neoJson = NearEarthObjectJSON(e.neo)
            json_object = CloseApproachJSON(e, neoJson)
            jsonString = json.dumps(
                json_object.__dict__, default=str, indent=4
            )
            if first_item:
                outfile.write(
                    json.dumps(json_object.__dict__, default=str, indent=4)
                )
                first_item = False
            else:
                outfile.write(
                    ","
                    + json.dumps(json_object.__dict__, default=str, indent=4)
                )
        outfile.write("]")
