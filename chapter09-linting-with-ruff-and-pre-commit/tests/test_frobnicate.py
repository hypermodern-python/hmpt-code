from hashlib import md5

import pytest


def frobnicate(s):
    return md5(s.encode()).hexdigest()


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("first test value",       "61df19525cf97aa3855b5aeb1b2bcb89"),
        ("another test value",     "5768979c48c30998c46fb21a91a5b266"),
        ("and here's another one", "e766977069039d83f01b4e3544a6a54c"),
    ]
)  # fmt: skip
def test_frobnicate(value, expected):
    assert expected == frobnicate(value)
