# slice-a-portion

[![PyPI](https://img.shields.io/pypi/v/slice-a-portion.svg)](https://pypi.org/project/slice-a-portion/)
[![Tests](https://github.com/mgaitan/slice-a-portion/actions/workflows/test.yml/badge.svg)](https://github.com/mgaitan/slice-a-portion/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/slice-a-portion?include_prereleases&label=changelog)](https://github.com/mgaitan/slice-a-portion/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/mgaitan/slice-a-portion/blob/main/LICENSE)

get the i/n slice of a sequence

## Installation

Install this library using `pip`:

```bash
pip install slice-a-portion
```


## Usage

There are two functions
```
>>> from slice_a_portion import slice_by_coefficients, slice_by_portion

```



```
   slice_by_coefficients(sequence: Sequence, start: Optional[float] = None, end: Optional[float] = None)
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
 ```

 ```
    slice_by_fraction(sequence: Sequence, i: int, n: int)
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
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd slice-a-portion
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
