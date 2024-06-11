from typing import Set, Union

from utils.Coverage import Location
from utils.ObjectUtils import dump_object, load_object, get_md5_of_object
import logging
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=os.path.join('logs', 'seeds_persistence.log'), filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str, _coverage: Set[Location], path: str = None, directory: str = './seeds') -> None:
        """Initialize from seed data"""
        self.energy = 0.0
        self.data = data
        if data is not None:
            self.id = get_md5_of_object(data)
            self.path = path if path else os.path.join(directory, f"{self.id}.seed")
            self.save(data, _coverage)
            self.coverage: Set[Location] = _coverage
        else:
            self.id = None
            self.path = path

    def __str__(self) -> str:
        data = self.load_data()
        return data if data else ''

    __repr__ = __str__

    def save(self, data: str, coverage: Set[Location], directory: str = './seeds') -> None:
        dump_object(self.path, {
            'data': data,
            'coverage': coverage
        })
        logger.info(f"Seed saved to {self.path}")

    def load_data(self) -> str:
        if not os.path.exists(self.path):
            logger.warning("Seed path is not set. Nothing to load.")
            raise (FileNotFoundError(f"Seed file not found: {self.path}"))
            return None
        seed = load_object(self.path)
        data = seed['data']
        logger.info(f"Seed data loaded from {self.path}")
        if data:
            return data
        else:
            return self.data

    def load_coverage(self) -> str:
        if not os.path.exists(self.path):
            logger.warning("Nothing to be loaded.")
            raise (FileNotFoundError(f"Seed not found: {self.path}"))
            return None
        seed = load_object(self.path)
        coverage = seed['coverage']
        logger.info(f"Seed coverage loaded from {self.path}")
        return coverage


