import numpy as np
from typing import Tuple

import tidepool_data_science_metrics.common.common as common


def gmi(bg_array, round_val=2):
    """
    Calculate the Glucose Management Indicator on set of glucose values. GMI indicates the average
    A1C level that would be expected based on mean glucose measured
    Reference - Glucose Management Indicator (GMI) - https://www.jaeb.org/gmi/

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Glucose Management Indicator
    """
    gmi = 3.31 + (0.02392 * common.mean(bg_array))
    return round(gmi, round_val)


def percent_values_by_range(
    bg_array, lower_threshold: int, upper_threshold: int, round_val=2
):
    """
    Calculate the percent of values that match has a bg within the lower and upper threshold.
    The lower and upper values will be included in the range to calculate on.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    lower_threshold : int
        The the lower value in the range to calculate on.
    upper_threshold : int
        zThe the upper value in the range to calculate on.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent value by range.
    """

    calc_low_thresh, calc_upper_thresh = _validate_input(
        lower_threshold, upper_threshold
    )
    results = round(
        np.where(
            (bg_array <= calc_upper_thresh) & (bg_array >= calc_low_thresh), 1, 0
        ).sum()
        / bg_array.size
        * 100,
        round_val,
    )
    return results


def percent_time_in_range_70_180(bg_array, round_val=2):
    """
    Calculate the percent of values with a blood glucose value between 70 and 180.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent value with in the range between 70 and 180.
    """
    return percent_values_by_range(
        bg_array, lower_threshold=70, upper_threshold=180, round_val=round_val
    )


def percent_time_above_180(bg_array, round_val=2):
    """
    Calculate the percent of values with a blood glucose above 180.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values above 180.
    """
    return percent_values_by_range(
        bg_array, lower_threshold=180, upper_threshold=1000, round_val=round_val
    )


def percent_time_below_70(bg_array, round_val=2):
    """
    Calculate the percent of values with a blood glucose below 70.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values below 70.
    """
    return percent_values_by_range(
        bg_array, lower_threshold=0, upper_threshold=70, round_val=round_val
    )


def percent_time_below_54(bg_array, round_val=2):
    """
    Calculate the percent of values with a blood glucose below 54.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values below 54.
    """
    return percent_values_by_range(
        bg_array, lower_threshold=0, upper_threshold=54, round_val=round_val
    )


def percent_time_above_250(bg_array, round_val=2):
    """
    Calculate the percent of values with a blood glucose above 250.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values above 250.
    """
    return percent_values_by_range(
        bg_array, lower_threshold=250, upper_threshold=0, round_val=round_val
    )


def episodes(bg_array, episodes_threshold: int, min_ct_per_ep=3, min_duration=5):
    """
    Calculate the number of episodes for a given set of glucose values based on provided thresholds.
    How the episode count it calculated.
    1. Identify all bg values that are within episode range.
    2. Find the array value that is in range and its next value after it is not in range.  This gives the index of the
    last bg in an potential episode.
    3. The next check looks at the value at the array index number based on min_ct_per_ep before the value from step 2.
    If that value is a 1 then we count this range as an "episode".

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    episodes_threshold : int
        Any bg values below this value will be considered as within the episode.
    min_ct_per_ep : int, optional
        The number of consecutive bg values required in the threshold range to be considered an episode.
    min_duration : int, optional (Not Implemented at this time.)
        The number of minutes expected between each bg value in the array. If there are gaps the code will .....

    Returns
    -------
    int
        The number of episodes matching input specifications.
    """
    check_string = "(in_range == 1) & (np.roll(in_range, -1) == 0) "
    i = min_ct_per_ep - 1
    while i > 0:
        check_string = check_string + f" & (np.roll(in_range, {i}) == 1) "
        i -= 1
    in_range = np.where(bg_array[:, 1] < episodes_threshold, 1, 0)
    episodes_count = np.count_nonzero(in_range[eval(check_string)])

    return episodes_count


def bgri(bg_array, round_val=2):
    """
    Calculate the LBGI, HBGI and BRGI within a set of glucose values from Clarke, W., & Kovatchev, B. (2009)

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with `int` type.
    round_val : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The number LBGI results.
    int
        The number HBGI results.
    int
        The number BRGI results.
    """
    bg_array[bg_array < 1] = 1  # this is added to take care of edge case BG <= 0
    transformed_bg = 1.509 * ((np.log(bg_array) ** 1.084) - 5.381)
    risk_power = 10 * (transformed_bg) ** 2
    low_risk_bool = transformed_bg < 0
    high_risk_bool = transformed_bg > 0
    rlBG = risk_power * low_risk_bool
    rhBG = risk_power * high_risk_bool
    LBGI = round(np.mean(rlBG), round_val)
    HBGI = round(np.mean(rhBG), round_val)
    BGRI = round(LBGI + HBGI, round_val)
    return LBGI, HBGI, BGRI


def _validate_input(lower_threshold: int, upper_threshold: int) -> Tuple[int, int]:
    if any(num < 0 for num in [lower_threshold, upper_threshold]):
        raise Exception("lower and upper thresholds must be a non-negative number")
    if upper_threshold == 0:
        upper_threshold = 1000
    if lower_threshold > upper_threshold:
        raise Exception("lower threshold is higher than the upper threshold.")
    return lower_threshold, upper_threshold
