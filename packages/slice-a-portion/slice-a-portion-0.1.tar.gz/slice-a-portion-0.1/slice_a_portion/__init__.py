from typing import Sequence, Optional


def slice_by_fraction(sequence: Sequence, i: int, n: int):
    """
    Split a sequence in `n` slices and then return the i-th (1-indexed).
    The last slice will be longer if the sequence can't be splitted even-sized or
    n is greater than the sequence's size.

    >>> from slice_a_portion import slice_by_fraction
    >>> slice_by_fraction("abcdefghi", 1, 2)
    'abcd'
    >>> slice_by_fraction("abcdefghi", 2, 2)
    'efghi'
    >>> slice_by_fraction("abcdefghi", 1, 3)
    'abc'
    >>> slice_by_fraction("abcdefghi", 2, 3)
    'def'
    >>> slice_by_fraction("abcdefghi", 3, 3)
    'ghi'        
    >>>
    """
    total = len(sequence)

    per_slice = total // n

    if not per_slice:
        return sequence if i == n else type(sequence)()

    ranges = [[n, n + per_slice] for n in range(0, total, per_slice)]

    # fix last
    if total % n != 0:
        ranges = ranges[:-1]
        ranges[-1][1] = None

    portion = dict(enumerate(ranges, 1))[i]
    return sequence[slice(*portion)]


def slice_by_coefficients(sequence: Sequence, start: Optional[float] = None, end: Optional[float] = None):
    """
    Return the slice between the coefficients `start` and `end`
    between 0 and 1.

    Corner elements may be repeated in consecutive slices.

    >>> slice_by_coefficients(abc", 0, 0.333)
    'a'
    >>> slice_by_coefficients("abc", 0.666, 1)
    'c'
    >>> slice_by_coefficients("abcd", 0, 0.499)
    'ab'
    >>> slice_by_coefficients("abcd", None, 0.499)
    'ab'
    >>> slice_by_coefficients("abcd", 0.5, 1)
    'cd'
    >>> slice_by_coefficients("abcd", 0.5)    # until the end
    'cd'
    """
    start = start or 0
    end = end or 1
    total = len(sequence)
    return sequence[slice(int(round(total * start)), int(total * end) + 1)]