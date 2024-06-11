from typing import Set, Union

from utils.Coverage import Location
from utils.ObjectUtils import dump_object, load_object, get_md5_of_object
import os

class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str, _coverage: Set[Location], dir: str = './seeds') -> None:
        """Initialize from seed data"""
        self.data = data

        # These will be needed for advanced power schedules
        self.coverage: Set[Location] = _coverage
        self.energy = 0.0
        self.id = get_md5_of_object(data)
        self.path = os.path.join(dir, f"{self.id}.seed")
        self.save(data, _coverage)
        # if data is not None:
        #     self.id = get_md5_of_object(data)
        #     self.path = os.path.join(directory, f"{self.id}.seed")
        #     self.save(data, _coverage)
        # else:
        #     self.id = None
        #     self.path = None


    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        data = self.load_data()
        return self.data

    __repr__ = __str__

    def save(self, data: str, coverage: Set[Location]) -> None:

        dump_object(self.path, {
            'data': data,
            'coverage': coverage
        })

    def load_data(self) -> str:

        seed = load_object(self.path)
        data = seed['data']
        return data

    def load_coverage(self) -> str:
        seed = load_object(self.path)
        coverage = seed['coverage']
        return coverage