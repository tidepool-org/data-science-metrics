from tidepool_data_science_metrics.common.common import mean, avg, std_deviation


def test_avg_glucose(bg_values):
    average = avg(bg_values)
    assert average == 86.48


def test_mean_glucose(bg_values):
    val = mean(bg_values)
    assert val == 86.48


def test_std_deviation(bg_values):
    std = std_deviation(bg_values)
    assert std == 11.90


def test_std_deviation_round(bg_values):
    std = std_deviation(bg_values, 3)
    assert std == 11.903
