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
import operator
from itertools import islice


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """_summary_ AttributeFilter."""

    def __init__(self, op, value):
        """_summary_.

        Args:
            op (_type_): _description_.
            value (_type_): _description_.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Raises:
            UnsupportedCriterionError: _description_.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__},value={self.value})"


class DateFilter(AttributeFilter):
    """_summary_.

    Args:
        AttributeFilter (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """_summary_.

    Args:
        AttributeFilter (_type_): _description_.

    Returns:
        _type_: _description_.

    """

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """_summary_.

    Args:
        AttributeFilter (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """_summary_.

    Args:
        AttributeFilter (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """_summary_.

    Args:
        AttributeFilter (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    @classmethod
    def get(cls, approach):
        """_summary_.

        Args:
            approach (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return approach.neo.hazardous


def create_filters(
    date=None,
    start_date=None,
    end_date=None,
    distance_min=None,
    distance_max=None,
    velocity_min=None,
    velocity_max=None,
    diameter_min=None,
    diameter_max=None,
    hazardous=None,
):
    """_summary_ create_filters.

    Args:
        date (_type_, optional):  A `date` on which a matching.
    `CloseApproach` occurs.. Defaults to None.
        start_date (_type_, optional): _description_. Defaults to None.
        end_date (_type_, optional): A `date` on or before which
    a matching `CloseApproach` occurs.. Defaults to None.
        distance_min (_type_, optional): _description_. Defaults to None.
        distance_max (_type_, optional): _description_. Defaults to None.
        velocity_min (_type_, optional): _description_. Defaults to None.
        velocity_max (_type_, optional): _description_. Defaults to None.
        diameter_min (_type_, optional): _description_. Defaults to None.
        diameter_max (_type_, optional): _description_. Defaults to None.
        hazardous (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main
    module with a value from the
    user's options at the command line.
    Each one corresponds to a different type
    of filter. For example, the `--date`
    option corresponds to the `date`
    argument, and represents a filter
    that selects close approaches that occurred
    on exactly that given date.
    Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with
    the `query` method of `NEODatabase`
    because the main module directly
    passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching
    `CloseApproach` occurs.
    :param start_date: A `date` on or after which
    a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which
    a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal
    approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal
    approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative
    approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative
    approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter
    of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter
    of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO o
    a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = ()
    if hazardous is not None:
        f = HazardousFilter(operator.eq, hazardous)
        filters += (f,)
    if date:
        f = DateFilter(operator.eq, date)
        filters += (f,)
    if start_date:
        f = DateFilter(operator.ge, start_date)
        filters += (f,)
    if end_date:
        f = DateFilter(operator.le, end_date)
        filters += (f,)
    if distance_min:
        f = DistanceFilter(operator.ge, distance_min)
        filters += (f,)
    if distance_max:
        f = DistanceFilter(operator.le, distance_max)
        filters += (f,)
    if velocity_min:
        f = VelocityFilter(operator.ge, velocity_min)
        filters += (f,)
    if velocity_max:
        f = VelocityFilter(operator.le, velocity_max)
        filters += (f,)
    if diameter_min:
        f = DiameterFilter(operator.ge, diameter_min)
        filters += (f,)
    if diameter_max:
        f = DiameterFilter(operator.le, diameter_max)
        filters += (f,)

    return filters


def limit(iterator, n=None):
    """If `n` is 0 or None, don't limit the iterator at all.

    Args:
        iterator (_type_): _description_.
        n (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_.
    """
    if n == 0:
        return iterator
    if n is None:
        return iterator
    print(islice(iterator, 0, n))
    return islice(iterator, 0, n)
