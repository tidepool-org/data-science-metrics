import pytest
import numpy as np
from tidepool_data_science_metrics.insulin.insulin import (
    approximate_steady_state_iob_from_sbr,
    dka_index,
    dka_risk_score,
)

def test_dka_index_with_zero_iob():
    for n_hours in range(0, 24):
        iob_array = np.zeros(n_hours * 12)  # an array that spans n_hours hours
        scheduled_basal_rate = 1.0  # U/hr
        dka_index_val = dka_index(iob_array, scheduled_basal_rate=scheduled_basal_rate, round_to_n_digits=1)
        assert dka_index_val == n_hours


def test_dka_index_with_exactly_50_percent_iob():
    for n_hours in range(0, 24):
        scheduled_basal_rate = 1.0  # U/hr
        iob = approximate_steady_state_iob_from_sbr(scheduled_basal_rate) / 2
        iob_array = np.ones(n_hours * 12) * iob # an array that spans n_hours hours
        dka_index_val = dka_index(iob_array, scheduled_basal_rate=scheduled_basal_rate, round_to_n_digits=1)
        assert dka_index_val == 0


def test_dkai_risk_scores():
    dkai_array = np.array([0, 1.9999, 2, 7.9, 8, 13.9999, 14, 14.00001, 20.9999, 21, 21.00001])
    dkai_rs = np.array([   0,      0, 1,   1, 2,       2,  3,        3,       3,  4,        4])
    for dkai, dkai_score in zip(dkai_array, dkai_rs):
        dkai_risk_score_val = dka_risk_score(dkai)
        assert dkai_risk_score_val == dkai_score
