from singleton import singleton
import math


@singleton
class StatisticsManager:
    compression_statistics = {}

    def __init__(self):
        pass

    def add_case(self, variables_count, source_complexity, result_complexity):
        if variables_count not in self.compression_statistics.keys():
            self.compression_statistics[variables_count] = []
        self.compression_statistics[variables_count].append((source_complexity, result_complexity))

    @staticmethod
    def print_statistics_for_cases(cases):
        medium = math.e**(sum(math.log(v[0] / v[1]) for v in cases) / len(cases))
        medium = int(medium * 10**2) / 10**2
        print(f"{medium} - medium compression level\n")
        maximum = max(v[0] / v[1] for v in cases)
        print(f"{maximum} - maximum compression level\n")
        minimum = min(v[0] / v[1] for v in cases)
        print(f"{minimum} - minimum compression level")

    def print_statistics(self):
        total_statistics = []
        for variables_count, results in self.compression_statistics.items():
            print(f"Statistics for cases with {variables_count} variables:\n")
            self.print_statistics_for_cases(results)
            total_statistics += results
        print("Statistics for all cases:\n")
        self.print_statistics_for_cases(total_statistics)


