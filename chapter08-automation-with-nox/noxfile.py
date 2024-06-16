import nox


@nox.session
@nox.parametrize(["a", "b"], [("1.0", "2.2"), ("0.9", "2.1")])
def tests(session, a, b):
    print(a, b)  # only the combinations listed above
