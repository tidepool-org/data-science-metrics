from tidepool_data_science_metrics.common.common import mean, avg, std_deviation
import numpy as np


def test_avg_glucose(bg_array):
    average = avg(bg_array)
    assert average == 86.48


def test_avg_glucose_round(bg_array):
    average = avg(bg_array, round_val=0)
    assert average == 86


def test_avg_glucose_weights(bg_values__3_values):
    average = avg(bg_values__3_values, weights=[[0], [1], [0]])
    assert average == 105


def test_mean_glucose(bg_array):
    val = mean(bg_array)
    assert val == 86.48


def test_std_deviation(bg_array):
    std = std_deviation(bg_array)
    assert std == 11.90


def test_std_deviation_round(bg_array):
    std = std_deviation(bg_array, 3)
    assert std == 11.903
