import numpy as np


def approximate_steady_state_iob_from_sbr(scheduled_basal_rate: np.float64) -> np.float64:
    """
    Approximate the amount of insulin-on-board from user's scheduled basal rate (sbr). This value
    comes from running the Tidepool Simple Diabetes Metabolism Model with the user's sbr for 8 hours.

    Parameters
    ----------
    scheduled_basal_rate : float
        a single value that represents the user's insulin needs
        NOTE: this needs to be updated to account for sbr schedule
    Returns
    -------
    float:
        insulin-on-board
    """
    # TODO: need test coverage here, which can be done by calling the diabetes metabolism model
    return scheduled_basal_rate * 2.111517


def dka_index(
    iob_array: "np.ndarray[np.float64]", scheduled_basal_rate: np.float64, round_to_n_digits: int = 3
) -> np.float64:
    """
    Calculate the Tidepool DKA Index, which is the number of hours with less than 50% of the
    user's normal insulin needs, assuming that their scheduled basal rate can be used as a proxy
    for their insulin needs.
    https://docs.google.com/document/d/1zrQK7tQ3OJzjOXbwDgmQEeCdcig49F2TpJzNk2FU52k

    Parameters
    ----------
    iob_array : ndarray
        1D array containing the insulin-on-board time series with float type.
    scheduled_basal_rate : float (U/hr)
        a single value that represents the user's insulin needs
        NOTE: this needs to be updated to account for sbr schedule
    round_to_n_digits : int, optional
        The number of digits to round the result to.

    Returns
    -------
    float
        The Tidepool DKA Index in hours.
    """
    # TODO: this funciton needs to be updated to allow for multiple scheduled basal rates, AKA schedules
    steady_state_iob = approximate_steady_state_iob_from_sbr(scheduled_basal_rate)
    fifty_percent_steady_state_iob = steady_state_iob / 2
    indices_with_less_50percent_sbr_iob = iob_array < fifty_percent_steady_state_iob
    hours_with_less_50percent_sbr_iob = np.sum(indices_with_less_50percent_sbr_iob) * 5 / 60

    return round(hours_with_less_50percent_sbr_iob, round_to_n_digits)


def dka_risk_score(hours_with_less_50percent_sbr_iob: np.float64) -> int:
    """
    Calculate the Tidepool DKA Risk Score
    https://docs.google.com/document/d/1zrQK7tQ3OJzjOXbwDgmQEeCdcig49F2TpJzNk2FU52k

    Parameters
    ----------
    hours_with_less_50percent_sbr_iob : float
        calculated from dka_index

    Returns
    -------
    int
        The Tidepool DKAI Risk Score.
    """
    if hours_with_less_50percent_sbr_iob >= 21:
        risk_score = 4
    elif hours_with_less_50percent_sbr_iob >= 14:
        risk_score = 3
    elif hours_with_less_50percent_sbr_iob >= 8:
        risk_score = 2
    elif hours_with_less_50percent_sbr_iob >= 2:
        risk_score = 1
    else:
        risk_score = 0
    return risk_score
