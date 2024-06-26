import time
import random
from typing import List, Tuple, Any

from fuzzer.GreyBoxFuzzer import GreyBoxFuzzer
from schedule.BlendPowerSchedule import BlendPowerSchedule
from runner.FunctionCoverageRunner import FunctionCoverageRunner

from utils.Seed import Seed


class BlendGreyBoxFuzzer(GreyBoxFuzzer):
    """Count how often individual paths are exercised."""

    def __init__(self, seeds: List[str], schedule: BlendPowerSchedule, is_print: bool):
        super().__init__(seeds, schedule, False)

        # TODO
        # self.paths = {}
        # self.schedule.paths = self.paths
        # self.schedule.results = {}
        self.last_path_time = self.start_time
        self.last_seed_time = time.time()

        print("""
┌───────────────────────┬───────────────────────┬───────────────────────┬───────────────────┬───────────────────┬────────────────┬───────────────────┐
│        Run Time       │     Last New Path     │    Last Uniq Crash    │    Total Execs    │    Total Paths    │  Uniq Crashes  │   Covered Lines   │
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤""")

    def print_stats(self):
        def format_seconds(seconds):
            hours = int(seconds) // 3600
            minutes = int(seconds % 3600) // 60
            remaining_seconds = int(seconds) % 60
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

        template = """│{runtime}│{path_time}│{crash_time}│{total_exec}│{total_path}│{uniq_crash}│{covered_line}│
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""
        template = template.format(runtime=format_seconds(time.time() - self.start_time).center(23),
                                   path_time=str(
                                       max([len(s.data) for s in self.population])).center(23),
                                   crash_time=format_seconds(
                                       self.last_crash_time - self.start_time).center(23),
                                   total_exec=str(self.total_execs).center(19),
                                   total_path=str(
                                       len(self.population)).center(19),
                                   uniq_crash=str(
                                       len(set(self.crash_map.values()))).center(16),
                                   covered_line=str(len(self.covered_line)).center(19))
        print(template)

    # type: ignore
    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:
        """Inform scheduler about path frequency"""
        result, outcome = super().run(runner)
        # TODO
        if self.schedule.update_path_freq(runner.coverage()):
            pass
            # self.population.append(Seed(self.inp, runner.coverage()))

        self.schedule.time[self.inp] = time.time() - self.last_seed_time
        self.last_seed_time = time.time()
        if outcome == runner.FAIL:
            self.schedule.fails.append(self.inp)
            self.population.append(Seed(self.inp, runner.coverage()))

        return result, outcome

    def create_candidate(self) -> str:
        """Returns an input generated by fuzzing a seed in the population"""
        seed = self.schedule.choose(self.population)

        # Stacking: Apply multiple mutations to generate the candidate
        candidate = seed.data
        trials = min(len(candidate), 1 << random.randint(1, 5))
        for i in range(trials):
            # if random.randint(0, 9):
            #     candidate = self.mutator.mutate(candidate)
            # else:
            #     candidate += self.mutator.mutate(candidate)
            candidate = self.mutator.mutate(candidate)

        return candidate
