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
        self.line_freq = {}
        # self.fails = []
        self.alpla = 1
        self.beta = 100
        # self.isNewPath = False

    def update_path_freq(self, path: Set[Location]):
        path = frozenset(path)
        if path in self.path_freq:
            self.path_freq[path] += 1
            return False
        else:
            self.path_freq[path] = 1
            return True
        
    def update_line_freq(self, line: Location):
        if line in self.line_freq:
            self.line_freq[line] += 1
            return False
        else:
            self.line_freq[line] = 1
            return True

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        # TODO
        # for seed in population:
        #     # self.update_path_freq(seed.coverage)
        #     # ranging [0, 1]
        #     path_freq = self.path_freq[frozenset(seed.coverage)] / sum(self.path_freq.values())
        #     seed.energy = math.exp(-self.alpla * path_freq)
        
        # # print(len(self.path_freq))

        seed_freq = {}
        for seed in population:
            seed_sum = 0
            for cov in seed.coverage:
                seed_sum += self.line_freq[cov]
            seed_freq[seed] = seed_sum / len(seed.coverage)

        for seed in seed_freq:
            seed.energy = self.beta * (1 - seed_freq[seed]/sum(seed_freq.values()))