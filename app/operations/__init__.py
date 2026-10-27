"""
Basic arithmetic operations for the FastAPI calculator.

Each function accepts ints or floats and returns the result. Every call is
logged so operations and errors can be traced in the application log.
"""

import logging
from typing import Union

Number = Union[int, float]

logger = logging.getLogger(__name__)


def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    result = a + b
    logger.debug("add(%s, %s) = %s", a, b, result)
    return result


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of a and b (a - b)."""
    result = a - b
    logger.debug("subtract(%s, %s) = %s", a, b, result)
    return result


def multiply(a: Number, b: Number) -> Number:
    """Return the product of a and b."""
    result = a * b
    logger.debug("multiply(%s, %s) = %s", a, b, result)
    return result


def divide(a: Number, b: Number) -> float:
    """
    Return the quotient of a and b (a / b).

    Raises:
        ValueError: if b is zero.
    """
    if b == 0:
        logger.error("divide(%s, %s) failed: division by zero", a, b)
        raise ValueError("Cannot divide by zero!")
    result = a / b
    logger.debug("divide(%s, %s) = %s", a, b, result)
    return result
