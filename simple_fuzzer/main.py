import os
import time
import random

from fuzzer.PathGreyBoxFuzzer import PathGreyBoxFuzzer
from fuzzer.BlendGreyBoxFuzzer import BlendGreyBoxFuzzer
from fuzzer.GreyBoxFuzzer import GreyBoxFuzzer
from runner.FunctionCoverageRunner import FunctionCoverageRunner
from schedule.PathPowerSchedule import PathPowerSchedule
from schedule.BlendPowerSchedule import BlendPowerSchedule
from schedule.AdvancedBlendPowerSchedule import AdvancedBlendPowerSchedule
from schedule.CoveragePowerSchedule import CoveragePowerSchedule
from samples.Samples import sample1, sample2, sample3, sample4
from utils.ObjectUtils import dump_object, load_object


class Result:
    def __init__(self, coverage, crashes, start_time, end_time):
        self.covered_line = coverage
        self.crashes = crashes
        self.start_time = start_time
        self.end_time = end_time

    # def __str__(self):
    #     return "Covered Lines: " + str(self.covered_line) + ", Crashes Num: " + str(self.crashes) + ", Start Time: " + str(self.start_time) + ", End Time: " + str(self.end_time)
    # 更直观的输出
    def __str__(self):
        return "Covered Lines Num: " + str(len(self.covered_line)) + ", Crashes Num: " + str(len(self.crashes)) + "\n\nCovered Lines: " + str(self.covered_line) + "\n\nCrashes Num: " + str(self.crashes) + "\nStart Time: " + str(self.start_time) + ", End Time: " + str(self.end_time) + "\n\nCovered Lines Num: " + str(len(self.covered_line)) + ", Crashes Num: " + str(len(self.crashes))

if __name__ == "__main__":
    # random.seed(42)
    random.seed(time.time())

    sample_list = [
        {"func": sample1, "seed":"corpus/corpus_1", "result":"Sample-1.pkl"},
        {"func": sample2, "seed":"corpus/corpus_2", "result":"Sample-2.pkl"},
        {"func": sample3, "seed":"corpus/corpus_3", "result":"Sample-3.pkl"},
        {"func": sample4, "seed":"corpus/corpus_4", "result":"Sample-4.pkl"},
    ]
    sample = sample_list[3]
    # f_runner = FunctionCoverageRunner(sample1)
    f_runner = FunctionCoverageRunner(sample["func"])
    seeds = load_object(sample["seed"])

    # grey_fuzzer = PathGreyBoxFuzzer(
    #     seeds=seeds, schedule=PathPowerSchedule(), is_print=True)
    # grey_fuzzer = BlendGreyBoxFuzzer(
    #     seeds=seeds, schedule=BlendPowerSchedule(), is_print=True)
    grey_fuzzer = GreyBoxFuzzer(
        seeds=seeds, schedule=CoveragePowerSchedule(), is_print=True)

    start_time = time.time()
    grey_fuzzer.runs(f_runner, run_time=600)
    res = Result(grey_fuzzer.covered_line, set(
        grey_fuzzer.crash_map.values()), start_time, time.time())
    dump_object("_result" + os.sep + sample["result"], res)
    print(load_object("_result" + os.sep + sample["result"]))
