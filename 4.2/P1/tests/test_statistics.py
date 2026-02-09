from statistics_core import mean, median, mode, variance_population


def test_mean():
    assert mean([1, 2, 3, 4]) == 2.5


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_variance():
    assert round(variance_population([1, 2, 3]), 5) == round(2 / 3, 5)
