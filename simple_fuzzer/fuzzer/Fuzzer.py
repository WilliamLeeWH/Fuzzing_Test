import subprocess
import time
from typing import Tuple, List

from runner.Runner import Runner

Outcome = str


class Fuzzer:
    """Base class for fuzzers."""

    def __init__(self) -> None:
        """Constructor"""
        self.start_time = time.time()
        self.total_execs = 0
        self.last_print_time = self.start_time

    def fuzz(self) -> str:
        """Return fuzz input"""
        return ""

    def print_stats(self):
        pass

    def run(self, runner: Runner = Runner()) \
            -> Tuple[subprocess.CompletedProcess, Outcome]:
        """Run `runner` with fuzz input"""
        res = runner.run(self.fuzz())
        self.total_execs += 1
        if time.time() - self.last_print_time > 1:
            self.print_stats()
            self.last_print_time = time.time()
        return res

    def runs(self, runner: Runner = Runner(), run_time: int = 60) \
            -> List[Tuple[subprocess.CompletedProcess, Outcome]]:
        """Run `runner` with fuzz input, `trials` times"""
        res = list()
        while time.time() - self.start_time < run_time:
            res.append(self.run(runner))
        return res
