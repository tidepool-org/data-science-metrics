import numpy as np
from typing import List


def mean(bg_array: "np.ndarray[np.int64]", round_to_ndigits: int = 2):
    """
    Calculate the mean within a set of glucose values

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_to_ndigits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Means
    """
    return round(np.mean(bg_array), round_to_ndigits)


def avg(
    bg_array: "np.ndarray[np.int64]",
    weights: List[int] = None,
    returned: bool = False,
    round_to_ndigits: int = 2,
):
    """
    Calculate the average within a set of glucose values

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    weights : array_like, optional
        An array of weights associated with the values in a. Each value in a contributes to the average according
        to its associated weight. The weights array can either be 1-D (in which case its length must be the size
        of a along the given axis) or of the same shape as a. If weights=None, then all data in a are assumed to
        have a weight equal to one.
    returned : bool, optional
        Default is False. If True, the tuple (average, sum_of_weights) is returned, otherwise only the average is
        returned. If weights=None, sum_of_weights is equivalent to the number of elements over which the average
        is taken.
    round_to_ndigits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Average
    """
    val = np.average(bg_array, weights=weights, returned=returned)
    return np.round(val, round_to_ndigits)


def std_deviation(bg_array: "np.ndarray[np.int64]", round_to_ndigits: int = 2):
    """
    Calculate the standard deviation within a set of glucose values

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_to_ndigits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        Calculated standard deviation
    """

    return round(np.std(bg_array), round_to_ndigits)


def coefficient_of_variation(
    bg_array: "np.ndarray[np.int64]", round_to_ndigits: int = 2
):
    """
    Calculate the coefficient of variation on set of glucose values

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_to_ndigits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Coefficient of variation
    """
    std_dev = std_deviation(bg_array, round_to_ndigits=round_to_ndigits)
    avg_glu = avg(bg_array, round_to_ndigits=round_to_ndigits)
    return round(std_dev / avg_glu * 100, round_to_ndigits)
