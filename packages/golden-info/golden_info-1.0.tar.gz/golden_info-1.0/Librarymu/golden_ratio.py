import math

class GoldenRatioCalculator:
    def calculate(self):
        return 1.618033988749895

def calculate_golden_ratio_recursive(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1.618033988749895
    else:
        return calculate_golden_ratio_recursive(n - 1) + calculate_golden_ratio_recursive(n - 2)

def calculate_golden_ratio_series(length):
    golden_ratio_series = [1, 1.618033988749895]
    for _ in range(2, length):
        next_value = golden_ratio_series[-1] + golden_ratio_series[-2]
        golden_ratio_series.append(next_value)
    return golden_ratio_series