import math

from typing import Dict, Sequence
from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed
from typing import Set
from utils.Coverage import Location


class PathPowerSchedule(PowerSchedule):

    def __init__(self) -> None:
        super().__init__()
        # TODO
        self.path_freq = {}
        self.alpla = 1
        self.crash = False

    def update_path_freq(self, path: Set[Location]):
        path = frozenset(path)
        if path in self.path_freq:
            self.path_freq[path] += 1
        else:
            self.path_freq[path] = 1

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        # TODO
        for seed in population:
            self.update_path_freq(seed.coverage)
            # ranging [0, 1]
            path_freq = self.path_freq[frozenset(seed.coverage)] / sum(self.path_freq.values())
            seed.energy = math.exp(-self.alpla * path_freq)
        
        

