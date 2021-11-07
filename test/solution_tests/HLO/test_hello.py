import pytest

from solutions.HLO import hello_solution


@pytest.mark.parametrize("name,expected", [
    ("John", "Hello, John!"),
    ("Tim", "Hello, Tim!"),
    ("", "Hello, !"),
])
def test_hello(name, expected):
    assert hello_solution.hello(name) == expected

