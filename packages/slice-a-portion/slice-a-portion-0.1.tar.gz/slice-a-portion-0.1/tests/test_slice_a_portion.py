from slice_a_portion import slice_by_fraction, slice_by_coefficients

import pytest


@pytest.mark.parametrize(
    "args, expected",
    [
        (("abc", 1, 7), ""),
        (("abc", 7, 7), "abc"),
        (("abc", 1, 1), "abc"),
        (("abcdefghi", 1, 2), "abcd"),
        (("abcdefghi", 2, 2), "efghi"),
        (("abcdefghi", 1, 3), "abc"),
        (("abcdefghi", 2, 3), "def"),
        (("abcdefghi", 3, 3), "ghi"),
        ((list("abcdefghijk"), 5, 5), ["i", "j", "k"]),
    ],
)
def test_slice_fraction(args, expected):
    assert slice_by_fraction(*args) == expected


@pytest.mark.parametrize(
    "seq, args, expected",
    [
        ("abc", (0, 0.333), "a"),
        ("abc", (0.333, 0.666), "b"),
        ("abc", (0.666, 1), "c"),
        ("abc", (0, 1), "abc"),  # all
        ("abcd", (0, 0.499), "ab"),
        ("abcd", (0.5, 1), "cd"),
        ("abcde", (0, 0.5), "abc"),  # c is repeated
        ("abcde", (0.5, 1), "cde"),
        ("abcdefghijk", (0, 0.5), "abcdef"),
        ("abcdefghijk", (None, 0.5), "abcdef"),
        ("abcdefghijk", (0.5, 1), "ghijk"),
        ("abcdefghijk", (0.5,), "ghijk"),
    ],
)
def test_slice_percentage(seq, args, expected):
    assert slice_by_coefficients(seq, *args) == expected
