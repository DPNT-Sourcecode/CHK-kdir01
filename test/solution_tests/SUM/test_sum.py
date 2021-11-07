import pytest

from solutions.SUM import sum_solution


@pytest.mark.parametrize("left,right,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (0, 100, 100),
    (100, 100, 200),
])
def test_sum(left, right, expected):
    assert sum_solution.compute(left, right) == expected

