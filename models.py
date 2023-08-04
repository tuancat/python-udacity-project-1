"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import json
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """_summary_.

    Returns:
        _type_: _description_.
    """

    def __init__(self, pdes, name, diameter, pha):
        """_summary_.

        Args:
            pdes (_type_): _description_.
            name (_type_): _description_.
            diameter (_type_): _description_.
            pha (_type_): _description_.
        """
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self.designation = pdes
        if len(name) == 0:
            self.name = None
        else:
            self.name = name
        try:
            if len(diameter) == 0:
                self.diameter = float("nan")
            else:
                self.diameter = float(diameter)
        except ValueError:
            self.diameter = float("nan")
        #    print 'Line {i} is corrupt!'.format(i = index)'

        if pha == "Y":
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return a representation of the full name of this NEO."""
        return self.designation

    def serialize(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        json = {
            "designation": self.designation,
            "name": self.name,
            "diameter": self.diameter,
            "hazardous": self.hazardous,
        }
        return json

    def __str__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        isNot = ""
        if self.hazardous:
            isNot = "is"
        else:
            isNot = " is not"
        return f"NEO {self.designation} has a diameter of {self.diameter:.3f} km and {isNot} potentially hazardous."

    def __repr__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """CloseApproach.

    Returns:
        _type_: _description_.
    """

    # If you make changes, be sure to update the comments in this file.
    def __init__(self, des, cd, dist, v_rel):
        """_summary_.

        Args:
            des (_type_): _description_.
            cd (_type_): _description_.
            dist (_type_): _description_.
            v_rel (_type_): _description_.
        """
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = des
        self.time = cd_to_datetime(cd)
        self.distance = float(dist)
        self.velocity = float(v_rel)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"At {self.time_str}, {self._designation}  approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """_summary_.

        Returns:
            _type_: _description_.
        """
        json = {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            # "neo": self.neo.toJSON
        }

        return json

    @property
    def datetime_utc(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        return self.time_str

    def default(self, o):
        """_summary_.

        Args:
            o (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return o.__dict__
