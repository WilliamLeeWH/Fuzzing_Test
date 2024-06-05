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
        self.beta = 2
        self.gamma = 5
        self.fails = []
        self.time = {}

    def assign_energy(self, population: Sequence[Seed]) -> None:
        # TODO
        for seed in population:
            seed.energy = 1
            seed.energy *= self.alpla * self.time[seed.data]/len(seed.data)
            # seed.energy *= math.exp(-self.beta * len(seed.data))
            seed.energy *= math.log(self.beta, len(seed.data))

            if seed.data in self.fails:
                seed.energy *= self.gamma
