from solutions.HLO import hello_solution


def test_hello():
    assert hello_solution.hello("Tim") == hello_solution.WELCOME_MESSAGE
