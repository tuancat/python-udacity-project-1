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
from extract import load_approaches, load_neos
from filters import create_filters, AttributeFilter


class NEODatabase:
    """_summary_."""

    def __init__(self, neos, approaches):
        """Highlights (blinks) a Selenium Webdriver element.

        Args:
            neos (_type_): _description_.
            approaches (_type_): _description_.
        """
        """Create a new `NEODatabase`.

        As a precondition,this constructor assumes the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        for e in self._approaches:
            neo = next(
                (
                    obj
                    for obj in self._neos
                    if obj.designation == e._designation
                ),
                None,
            )
            if neo is not None:
                e.neo = neo
        for e in self._neos:
            for e1 in self._approaches:
                if e.designation == e1._designation:
                    e.approaches.append(e1)

        self.neosDictByDesignation = {}
        self.neosDictByName = {}
        for e in self._neos:
            self.neosDictByDesignation[str(e.designation)] = e
            self.neosDictByName[str(e.name)] = e

    def get_neo_by_designation(self, designation):
        """_summary_.

        Args:
            designation (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        return self.neosDictByDesignation.get(designation)

    def get_neo_by_name(self, name):
        """get_neo_by_name_.

        Args:
            name (_type_): The name, as a string, of the NEO to search for.

        Returns:
            _type_:The `NearEarthObject` with the desired name, or `None`.

        """
        return self.neosDictByName.get(name)

    def query(self, filters=()):
        """query_.

        Args:
            filters (tuple, optional): _description_. A collection of filters capturing user-specified criteria.
        Returns:
            _type_: A stream of matching `CloseApproach` objects.

        """
        if len(filters) == 0:
            return self._approaches
        result = filter(
            lambda approach: all(f(approach) for f in filters),
            self._approaches,
        )
        return result


def main():
    """_summary_."""
    neos = load_neos("data/neos.csv")
    approaches = load_approaches("data/cad.json")
    dao = NEODatabase(neos, approaches)
    result = dao.query()
    print(len(dao._approaches))
    print(result)


if __name__ == "__main__":
    main()
