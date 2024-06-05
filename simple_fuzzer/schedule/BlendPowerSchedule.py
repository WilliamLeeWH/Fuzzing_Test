import math

from typing import Dict, Sequence
from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed
from typing import Set
from utils.Coverage import Location


class BlendPowerSchedule(PowerSchedule):

    def __init__(self) -> None:
        super().__init__()
        # TODO
        self.paths = {}
        self.alpla = 100
        self.beta = 20
        self.gamma = 5
        self.delta = 2
        self.fails = []
        self.time = {}

    def update_path_freq(self, path: Set[Location]):
        path = frozenset(path)
        if path in self.paths:
            self.paths[path] += 1
            return False
        else:
            self.paths[path] = 1
            return True

    def assign_energy(self, population: Sequence[Seed]) -> None:
        # TODO
        for seed in population:
            if len(seed.data) <= 1:
                seed.energy = 0
                continue
            seed.energy = 1.0

            path_freq = self.paths[frozenset(
                seed.coverage)] / sum(self.paths.values())

            if seed.data in self.fails:
                seed.energy *= math.exp(self.gamma)
            else:
                seed.energy *= math.exp(-self.delta * path_freq)

            seed.energy *= self.alpla * self.time[seed.data]/len(seed.data)
            try:
                seed.energy *= math.log(self.beta, len(seed.data))
            except:
                print(self.beta, len(seed.data))