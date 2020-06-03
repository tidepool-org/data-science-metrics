import numpy as np
from typing import Tuple
import warnings
import operator
import tidepool_data_science_metrics.common.common as common

# TODO: allow these functions to take in a mmol/L in addition to mg/dL
# TODO: allow these functions to operate on a matrix of glucose column arrays


def glucose_management_index(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the Glucose Management Indicator on set of glucose values. GMI indicates the average
    A1C level that would be expected based on mean glucose measured
    Reference - Glucose Management Indicator (GMI) - https://www.jaeb.org/gmi/

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    float
        The calculated Glucose Management Indicator
    """
    _validate_bg(bg_array)
    gmi = 3.31 + (0.02392 * common.mean(bg_array))
    return round(gmi, round_to_n_digits)


def percent_values_by_range(
    bg_array: "np.ndarray[np.float64]",
    lower_bound: int == 1,
    upper_bound: int == 1000,
    lower_bound_operator: object = operator.ge,
    upper_bound_operator: object = operator.lt,
    round_to_n_digits: int = 3,
) -> np.float64:
    """
    Calculate the percent of bg values are within the specified range.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with float or int type.
    lower_bound_operator : operator object
        operators include:
            operator.ge (greater than or equal to) DEFAULT
            operator.gt (greater than)
    lower_bound : int
        The the lower bound in the calculation range.
    upper_bound_operator : operator object
        operators include:
            operator.lt (less than) DEFAULT
            operator.le (less than or equal to)
    upper_bound : int
        The the upper bound in the calculation range.
    round_to_n_digits : int
        The number of digits to round the result to. DEFAULT = 3

    Returns
    -------
    float
        The percentage of values in the specified range.
    """

    _validate_bg(bg_array)
    _validate_input(lower_bound, upper_bound)
    n_meet_criteria = sum(lower_bound_operator(bg_array, lower_bound) & upper_bound_operator(bg_array, upper_bound))
    percent_meet_criteria = n_meet_criteria / len(bg_array) * 100
    rounded_percent = np.round(percent_meet_criteria, round_to_n_digits)

    return rounded_percent


def percent_values_ge_70_le_180(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values with a glucose values that are
    greater-than-or-equal-to (ge) 70 and less-than-or-equal-to (le) 180 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with float or int type.
    round_to_n_digits : int
        The number of digits to round the result to. DEFAULT = 3

    Returns
    -------
    float
        The percent value with in the range between 70 and 180 mg/dL.
    """
    return percent_values_by_range(
        bg_array,
        lower_bound_operator=operator.ge,
        lower_bound=70,
        upper_bound_operator=operator.le,
        upper_bound=180,
        round_to_n_digits=round_to_n_digits,
    )


def percent_values_lt_70(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values less than (lt) 70 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values below 70.
    """
    return percent_values_by_range(
        bg_array, lower_bound=1, upper_bound=70, upper_bound_operator=operator.lt, round_to_n_digits=round_to_n_digits,
    )


def percent_values_lt_54(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values less than (lt) 54 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    float
        The percent values less than 54 mg/dL.
    """
    _validate_bg(bg_array)
    return percent_values_by_range(
        bg_array, lower_bound=1, upper_bound=54, upper_bound_operator=operator.lt, round_to_n_digits=round_to_n_digits,
    )


def percent_values_lt_40(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values less than (lt) 40 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    float
        The percent values less than 54 mg/dL.
    """
    _validate_bg(bg_array)
    return percent_values_by_range(
        bg_array, lower_bound=1, upper_bound=40, upper_bound_operator=operator.lt, round_to_n_digits=round_to_n_digits,
    )


def percent_values_gt_180(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values greater than (gt) 180 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    float
        The percent values above 180.
    """
    return percent_values_by_range(
        bg_array,
        lower_bound=180,
        upper_bound=1000,
        lower_bound_operator=operator.gt,
        round_to_n_digits=round_to_n_digits,
    )


def percent_values_gt_250(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values greater than (gt) 250 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values greater than (gt) 250.
    """
    return percent_values_by_range(
        bg_array,
        lower_bound=250,
        upper_bound=1000,
        lower_bound_operator=operator.gt,
        round_to_n_digits=round_to_n_digits,
    )


def percent_values_gt_300(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values greater than (gt) 300 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values greater than (gt) 300.
    """
    return percent_values_by_range(
        bg_array,
        lower_bound=300,
        upper_bound=1000,
        lower_bound_operator=operator.gt,
        round_to_n_digits=round_to_n_digits,
    )


def percent_values_gt_400(bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 3) -> np.float64:
    """
    Calculate the percent of values greater than (gt) 400 mg/dL.

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    int
        The percent values greater than (gt) 400.
    """
    return percent_values_by_range(
        bg_array,
        lower_bound=400,
        upper_bound=1000,
        lower_bound_operator=operator.gt,
        round_to_n_digits=round_to_n_digits,
    )


def episodes(
    bg_array: "np.ndarray[np.float64]", episodes_threshold: int, min_ct_per_ep: int = 3, min_duration: int = 5,
) -> np.float64:
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
        1D array containing data with  float or int type.
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
    _validate_bg(bg_array)
    check_string = "(in_range == 1) & (np.roll(in_range, -1) == 0) "
    i = min_ct_per_ep - 1
    while i > 0:
        check_string = check_string + f" & (np.roll(in_range, {i}) == 1) "
        i -= 1
    in_range = np.where(bg_array < episodes_threshold, 1, 0)
    episodes_count = np.count_nonzero(in_range[eval(check_string)])

    return episodes_count


def blood_glucose_risk_index(
    bg_array: "np.ndarray[np.float64]", round_to_n_digits: int = 2
) -> Tuple[float, float, float]:
    """
    Calculate the LBGI, HBGI and BRGI within a set of glucose values from Clarke, W., & Kovatchev, B. (2009)

    Parameters
    ----------
    bg_array : ndarray
        1D array containing data with  float or int type.
    round_to_n_digits : int, optional
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
    _validate_bg(bg_array)
    bg_array[bg_array < 1] = 1  # this is added to take care of edge case BG <= 0
    transformed_bg = 1.509 * ((np.log(bg_array) ** 1.084) - 5.381)
    risk_power = 10 * (transformed_bg ** 2)
    low_risk_bool = transformed_bg < 0
    high_risk_bool = transformed_bg > 0
    rlBG = risk_power * low_risk_bool
    rhBG = risk_power * high_risk_bool
    lbgi = np.mean(rlBG)
    hbgi = np.mean(rhBG)
    bgri = round(lbgi + hbgi, round_to_n_digits)
    return (
        round(lbgi, round_to_n_digits),
        round(hbgi, round_to_n_digits),
        bgri,
    )


def lbgi_risk_score(lbgi: np.float64) -> int:
    """
    Calculate the Tidepool Risk Score associated with the LBGI
    https://docs.google.com/document/d/1EfIqZPsk_aF6ccm2uxO8Kv6677FIZ7SgjAAX6CmRWOM/

    Parameters
    ----------
    lbgi : float
        LBGI value calculated from BGRI

    Returns
    -------
    int
        The Tidepool LBGI Risk Score.
    """
    if lbgi > 10:
        risk_score = 4
    elif lbgi > 5:
        risk_score = 3
    elif lbgi > 2.5:
        risk_score = 2
    elif lbgi > 0:
        risk_score = 1
    else:
        risk_score = 0
    return risk_score


def _validate_input(lower_threshold: int, upper_threshold: int) -> Tuple[int, int]:
    if any(num < 0 for num in [lower_threshold, upper_threshold]):
        raise Exception("lower and upper thresholds must be a non-negative number")
    if lower_threshold > upper_threshold:
        raise Exception("lower threshold is higher than the upper threshold.")
    return


def _validate_bg(bg_array: "np.ndarray[np.float64]"):
    if (bg_array < 38).any():
        warnings.warn("Some values in the passed in array had glucose values less than 38.")

    if (bg_array > 402).any():
        warnings.warn("Some values in the passed in array had glucose values greater than 402.")

    if (bg_array < 1).any():
        raise Exception("Some values in the passed in array had glucose values less than 1.")

    if (bg_array > 1000).any():
        raise Exception("Some values in the passed in array had glucose values greater than 1000.")
