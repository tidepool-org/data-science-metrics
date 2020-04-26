import numpy as np
from typing import Tuple

import tidepool_data_science_metrics.common.common as common


def cv_of_glucose(bg_values, round_val=2):
    """
    Calculate the coefficient of variation on set of glucose values

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Coefficient of variation
    """
    std_dev = common.std_deviation(bg_values, round_val)
    avg_glu = common.avg(bg_values, round_val)
    return round(std_dev / avg_glu * 100, round_val)


def gmi(bg_values, round_val=2):
    """
    Calculate the Glucose Management Indicator on set of glucose values. GMI indicates the average
    A1C level that would be expected based on mean glucose measured

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        The calculated Glucose Management Indicator
    """
    gmi = 3.31 + (0.02392 * common.mean(bg_values))
    return round(gmi, round_val)


def percent_values_by_range(
    bg_values, lower_threshold: int, upper_threshold: int, round_val=2
):
    """
    Calculate the percent of values that match has a bg within the lower and upper threshold.
    The lower and upper values will be included in the range to calculate on.

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    lower_threshold : int
        The the lower value in the range to calculate on.
    upper_threshold : int
        zThe the upper value in the range to calculate on.
    round_val : int
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
            (bg_values <= calc_upper_thresh) & (bg_values >= calc_low_thresh), 1, 0
        ).sum()
        / bg_values.size
        * 100,
        round_val,
    )
    return results


def percent_time_in_range(
    bg_values, lower_threshold: int, upper_threshold: int, round_val=2, time_delta=5
):

    calc_low_thresh, calc_upper_thresh = _validate_input(
        lower_threshold, upper_threshold
    )
    bg_df = bg_values["bg_values"]
    bg_np = bg_df.to_numpy()
    in_range = np.count_nonzero((bg_np > calc_low_thresh) & (bg_np < calc_upper_thresh))
    val_count = bg_df.count()
    return round(in_range / val_count * 100, round_val)


def episodes(
    bg_values_df, episodes_threshold: int, min_ct_per_ep=3, min_duration=5, round_val=2
):
    """
    Calculate the number of episodes for a given set of glucose values based on provided thresholds.

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    lower_threshold : int
        The the lower value in the range to calculate on.
    upper_threshold : int
        zThe the upper value in the range to calculate on.
    round_val : int
        The number of digits to round the result to.

    Returns
    -------
    int
        The number of episodes matching input specifications.
    """
    bg_values_df.loc[(bg_values_df["values"] < episodes_threshold), "episode"] = 1
    bg_values_df.loc[(bg_values_df["values"] >= episodes_threshold), "episode"] = 0
    bg_values_df["group"] = 0
    bg_values_df["group"][
        (
            (bg_values_df.episode == 1)
            & (bg_values_df.episode.shift(1) == 0)
            & (bg_values_df.episode.shift(-1) == 1)
            & (bg_values_df.episode.shift(-(min_ct_per_ep - 1)) == 1)
        )
    ] = 1
    bg_values_df["group"][
        (
            (bg_values_df.episode == 1)
            & (bg_values_df.index == 0)
            & (bg_values_df.episode.shift(-1) == 1)
            & (bg_values_df.episode.shift(-2) == 1)
        )
    ] = 1
    group_sum = sum(bg_values_df.group)
    return group_sum


def bgri(bg_values, round_val=2):
    """
    Calculate the LBGI, HBGI and BRGI within a set of glucose values from Clarke, W., & Kovatchev, B. (2009)

    Parameters
    ----------
    bg_values : ndarray
        1D array containing data with `int` type.
    round_val : int
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
    bg_values[bg_values < 1] = 1  # this is added to take care of edge case BG <= 0
    transformed_bg = 1.509 * ((np.log(bg_values) ** 1.084) - 5.381)
    risk_power = 10 * (transformed_bg) ** 2
    low_risk_bool = transformed_bg < 0
    high_risk_bool = transformed_bg > 0
    rlBG = risk_power * low_risk_bool
    rhBG = risk_power * high_risk_bool
    LBGI = round(np.mean(rlBG), round_val)
    HBGI = round(np.mean(rhBG), round_val)
    BGRI = round(LBGI + HBGI, round_val)

    return LBGI[0], HBGI[0], BGRI[0]


def _validate_input(lower_threshold: int, upper_threshold: int) -> Tuple[int, int]:
    if any(num < 0 for num in [lower_threshold, upper_threshold]):
        raise Exception("lower and upper thresholds must be a non-negative number")
    if upper_threshold == 0:
        upper_threshold = 1000
    if lower_threshold > upper_threshold:
        raise Exception("lower threshold is higher than the upper threshold.")
    return lower_threshold, upper_threshold
