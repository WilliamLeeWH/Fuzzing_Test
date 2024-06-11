from typing import Dict, List

from typing import List, Any
from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed
import hashlib
import pickle

def get_path_id(coverage: Any) -> str:
    pickled = pickle.dumps(sorted(coverage))
    return hashlib.md5(pickled).hexdigest()
from utils.Seed import Seed

class CoveragePowerSchedule(PowerSchedule):
    
    def __init__(self) -> None:
        super().__init__()
        self.path_frequency: Dict[str, int] = {}
        self.novelty_scores: Dict[str, float] = {}

    def assign_energy(self, population: List[Seed]) -> None:
        """Assign higher energy to seeds that cover more lines of code"""
        for seed in population:
            path_id = get_path_id(seed.load_coverage())
            # Check if path_id is in path_frequency, if not initialize it
            if path_id not in self.path_frequency:
                self.path_frequency[path_id] = 0
            self.path_frequency[path_id] += 1

            # Update novelty score
            if path_id not in self.novelty_scores:
                self.novelty_scores[path_id] = 1 / self.path_frequency[path_id]
            else:
                self.novelty_scores[path_id] = 1 / self.path_frequency[path_id]

            seed.energy = self.novelty_scores[path_id]
