import nox


@nox.session
@nox.parametrize("a", ["1.0", "0.9"])
@nox.parametrize("b", ["2.2", "2.1"])
def tests(session, a, b):
    print(a, b)  # all combinations of a and b
