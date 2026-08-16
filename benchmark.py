import time


class Benchmark:
    def __init__(self, analyzer, repeat=10):
        self.analyzer = analyzer
        self.repeat = repeat

    def measure(self, pattern, filter_data):
        total_time = 0.0

        for _ in range(self.repeat):
            start = time.perf_counter()

            self.analyzer.mac_calculate(
                pattern,
                filter_data
            )

            end = time.perf_counter()

            total_time += end - start

        average_ms = (
            total_time / self.repeat
        ) * 1000

        size = len(pattern)
        operation_count = size * size

        return average_ms, operation_count