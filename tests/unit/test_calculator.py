"""Unit tests for app/operations: every function, including edge cases."""

import logging

import pytest

from app.operations import add, divide, multiply, subtract


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (-2, -3, -5),
        (-2, 3, 1),
        (0, 0, 0),
        (2.5, 3.5, 6.0),
        (1e10, 1e10, 2e10),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),
        (3, 5, -2),
        (-5, -3, -2),
        (0, 0, 0),
        (5.5, 2.25, 3.25),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (-2, -3, 6),
        (0, 100, 0),
        (2.5, 4, 10.0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),
        (-6, 3, -2.0),
        (-6, -3, 2.0),
        (0, 5, 0.0),
        (7, 2, 3.5),
        (1, 3, 0.3333333333),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a", [1, 0, -5, 2.5])
def test_divide_by_zero_raises(a):
    with pytest.raises(ValueError, match="Cannot divide by zero!"):
        divide(a, 0)


def test_divide_returns_float():
    assert isinstance(divide(4, 2), float)


def test_divide_by_zero_is_logged(caplog):
    with caplog.at_level(logging.ERROR, logger="app.operations"):
        with pytest.raises(ValueError):
            divide(10, 0)
    assert "division by zero" in caplog.text


def test_operations_log_results(caplog):
    with caplog.at_level(logging.DEBUG, logger="app.operations"):
        add(1, 2)
        subtract(5, 1)
        multiply(2, 4)
        divide(9, 3)
    assert "add(1, 2) = 3" in caplog.text
    assert "subtract(5, 1) = 4" in caplog.text
    assert "multiply(2, 4) = 8" in caplog.text
    assert "divide(9, 3) = 3.0" in caplog.text
