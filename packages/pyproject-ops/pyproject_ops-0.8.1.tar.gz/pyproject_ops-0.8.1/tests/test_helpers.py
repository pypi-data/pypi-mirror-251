# -*- coding: utf-8 -*-

import pytest
from pyproject_ops.helpers import (
    extract_digit_tokens,
    identify_py_major_and_minor_version,
    bump_version,
)


def test_extract_digit_tokens():
    assert extract_digit_tokens("^1.23.456.*") == ["1", "23", "456"]


def test_identify_py_major_and_minor_version():
    assert identify_py_major_and_minor_version("3.8") == (3, 8)
    assert identify_py_major_and_minor_version("3.8.*") == (3, 8)
    assert identify_py_major_and_minor_version("^3.8") == (3, 8)
    assert identify_py_major_and_minor_version("~3.8") == (3, 8)
    assert identify_py_major_and_minor_version(">=3.8") == (3, 8)

    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("abc")
    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("<3.10")
    with pytest.raises(ValueError):
        identify_py_major_and_minor_version("3")


def test_bump_version():
    assert bump_version("1.2.3", major=True) == "2.0.0"
    assert bump_version("1.2.3", minor=True) == "1.3.0"
    assert bump_version("1.2.3", patch=True) == "1.2.4"

    with pytest.raises(ValueError):
        bump_version("1.2.3", major=True, minor=True, patch=True)


if __name__ == "__main__":
    from pyproject_ops.tests import run_cov_test

    run_cov_test(__file__, "pyproject_ops.helpers", preview=False)
