import pandas as pd
from tidepool_data_science_metrics.common.common import mean, avg, std_deviation


def test_avg_glucose():
    pd_values = get_values()
    average = avg(pd_values.to_numpy())
    assert average == 86.48


def test_mean_glucose():
    pd_values = get_values()
    val = mean(pd_values.to_numpy())
    assert val == 86.48


def test_std_deviation():
    pd_values = get_values()
    std = std_deviation(pd_values.to_numpy())
    assert std == 11.90


def test_std_deviation_round():
    pd_values = get_values()
    std = std_deviation(pd_values.to_numpy(), 3)
    assert std == 11.903


# 100 values
def get_values():
    values = [
        [100],
        [105],
        [108],
        [104],
        [101],
        [106],
        [100],
        [105],
        [105],
        [99],
        [96],
        [101],
        [86],
        [85],
        [80],
        [83],
        [80],
        [82],
        [73],
        [74],
        [73],
        [73],
        [78],
        [76],
        [76],
        [71],
        [75],
        [77],
        [76],
        [74],
        [75],
        [76],
        [85],
        [82],
        [82],
        [83],
        [85],
        [84],
        [92],
        [92],
        [87],
        [97],
        [94],
        [94],
        [100],
        [101],
        [103],
        [100],
        [105],
        [105],
        [112],
        [103],
        [102],
        [98],
        [105],
        [105],
        [97],
        [97],
        [100],
        [98],
        [98],
        [93],
        [90],
        [86],
        [86],
        [88],
        [87],
        [83],
        [81],
        [84],
        [82],
        [83],
        [80],
        [76],
        [74],
        [82],
        [75],
        [71],
        [80],
        [76],
        [74],
        [72],
        [79],
        [79],
        [80],
        [77],
        [80],
        [76],
        [79],
        [76],
        [83],
        [81],
        [86],
        [82],
        [84],
        [84],
        [80],
        [70],
        [60],
        [50],
    ]
    return pd.DataFrame(values, columns=["bg_values"])
