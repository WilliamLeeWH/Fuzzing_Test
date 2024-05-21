import hashlib
import traceback
from typing import Tuple, Callable, Set, Any, List

from runner.Runner import Runner
from utils.Coverage import Coverage, Location


class FunctionCoverageRunner(Runner):
    def __init__(self, function: Callable) -> None:
        """Initialize.  `function` is a function to be executed"""
        self._coverage = None
        self.function = function
        self.cumulative_coverage: List[int] = []
        self.all_coverage: Set[Location] = set()
        
    def run_function(self, inp: str) -> Any:
        with Coverage() as cov:
            try:
                result = self.function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        self.all_coverage |= cov.coverage()
        self.cumulative_coverage.append(len(self.all_coverage))
        return result

    def coverage(self) -> Set[Location]:
        return self._coverage
    
    def run(self, inp: str) -> Tuple[Any, str]:
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception as exc:
            stack_trace = "".join(traceback.format_tb(exc.__traceback__))
            result = hashlib.md5(stack_trace.encode()).hexdigest()
            outcome = self.FAIL

        return result, outcome
