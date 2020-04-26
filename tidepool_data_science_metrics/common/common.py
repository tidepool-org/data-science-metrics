import numpy as np


def mean(bg_values, round_val=2):
    """
    Calculate the mean within a set of glucose values

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Means
    """
    return round(np.mean(bg_values), round_val)


def avg(bg_values, round_val=2):
    """
    Calculate the average within a set of glucose values

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Average
    """

    return round(np.average(bg_values), round_val)


def std_deviation(bg_values, round_val=2):
    """
    Calculate the standard deviation within a set of glucose values

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        Calculated standard deviation
    """

    return round(np.std(bg_values), round_val)
