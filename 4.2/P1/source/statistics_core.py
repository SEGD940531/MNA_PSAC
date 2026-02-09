import math
from typing import List, Dict


def mean(data: List[float]) -> float:
    total = 0.0
    for value in data:
        total += value
    return total / len(data)


def median(data: List[float]) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)

    if n % 2 == 1:
        return sorted_data[n // 2]

    mid1 = sorted_data[n // 2 - 1]
    mid2 = sorted_data[n // 2]
    return (mid1 + mid2) / 2


def mode(data: List[float]) -> List[float]:
    freq: Dict[float, int] = {}

    for value in data:
        if value in freq:
            freq[value] += 1
        else:
            freq[value] = 1

    max_count = max(freq.values())
    modes = []

    for key, count in freq.items():
        if count == max_count:
            modes.append(key)

    return modes


def variance_population(data: List[float]) -> float:
    avg = mean(data)
    total = 0.0

    for value in data:
        total += (value - avg) ** 2

    return total / len(data)


def std_population(data: List[float]) -> float:
    return math.sqrt(variance_population(data))