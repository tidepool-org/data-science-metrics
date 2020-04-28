import pandas as pd
import numpy as np
import pytest
from tidepool_data_science_metrics.cgm.cgm import (
    percent_values_by_range,
    percent_time_in_range,
    cv_of_glucose,
    gmi,
    bgri,
    episodes,
)
import datetime


def test_calculation(bg_values):
    percent = percent_values_by_range(bg_values, 100, 0)
    assert 22.0 == percent


def test_invalid_lower_number(bg_values):
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(bg_values, -1, 0)
    assert "lower and upper thresholds must be a non-negative number" in str(
        excinfo.value
    )


def test_invalid_upper_number(bg_values):
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(bg_values, 0, -1)
    assert "lower and upper thresholds must be a non-negative number" in str(
        excinfo.value
    )


def test_missing_lower_number(bg_values):
    with pytest.raises(TypeError) as excinfo:
        percent = percent_values_by_range(bg_values, 100)


def test_lower_number_higher_than_upper_number(bg_values):
    with pytest.raises(Exception) as excinfo:
        percent = percent_values_by_range(bg_values, 100, 20)
    print(str(excinfo.value))
    assert "lower threshold is higher than the upper threshold." in str(excinfo.value)


def test_percent_time_in_range():
    percent = percent_time_in_range(get_date_values(), 100, 150)
    assert percent == 47.06


def test_percent_time_in_range_round():
    percent = percent_time_in_range(get_date_values(), 100, 150, 3)
    assert percent == 47.059


def test_gmi(bg_values):
    gmi_value = gmi(bg_values)
    assert gmi_value == 5.38


def test_gmi_round(bg_values):
    gmi_value = gmi(bg_values, 3)
    assert gmi_value == 5.379


def test_cv_of_glucose(bg_values):
    std = cv_of_glucose(bg_values)
    assert std == 13.76


def test_cv_of_glucose_round(bg_values):
    std = cv_of_glucose(bg_values, 3)
    assert std == 13.764


def test_get_bgri(bg_values):
    LBGI, HBGI, BGRI = bgri(bg_values)
    assert BGRI == 3.25
    assert HBGI == 0.0
    assert LBGI == 3.25


def test_get_bgri_round(bg_values):
    LBGI, HBGI, BGRI = bgri(bg_values, 3)
    assert BGRI == 3.245
    assert HBGI == 0.0
    assert LBGI == 3.245


def test_get_episodes_3_consecutive():
    pd_values = get_date_ep_values()
    std = episodes(pd_values, 55, 3)
    assert std == 2


def test_get_episodes_4_consecutive():
    pd_values = get_date_ep_values()
    std = episodes(pd_values, 55, 4)
    assert std == 1


def get_date_values():
    values = [
        ["8/15/2019 00:40:00", 87],
        ["8/15/2019 00:45:00", 90],
        ["8/15/2019 01:55:00", 104],
        ["8/15/2019 00:50:00", 92],
        ["8/15/2019 00:55:00", 96],
        ["8/15/2019 01:00:00", 94],
        ["8/15/2019 01:05:00", 97],
        ["8/15/2019 01:10:00", 95],
        ["8/15/2019 01:15:00", 100],
        ["8/15/2019 01:20:00", 102],
        ["8/15/2019 01:25:00", 101],
        ["8/15/2019 01:30:00", 105],
        ["8/15/2019 01:35:00", 80],
        ["8/15/2019 01:40:00", 103],
        ["8/15/2019 01:45:00", 108],
        ["8/15/2019 01:50:00", 103],
        ["8/16/2019 02:00:00", 108],
    ]

    new_array = []
    for i in values:
        date = datetime.datetime.strptime(i[0], "%m/%d/%Y %H:%M:%S")
        new_array.append([date, i[1]])
    return pd.DataFrame(new_array, columns=["date", "bg_values"])


def get_date_ep_values():
    return np.array(
        [
            ["8/15/2019 00:40:00", 87],
            ["8/15/2019 00:45:00", 90],
            ["8/15/2019 00:50:00", 44],
            ["8/15/2019 00:55:00", 46],
            ["8/15/2019 01:00:00", 51],
            ["8/15/2019 01:05:00", 97],
            ["8/15/2019 01:10:00", 95],
            ["8/15/2019 01:15:00", 100],
            ["8/15/2019 01:20:00", 54],
            ["8/15/2019 01:25:00", 101],
            ["8/15/2019 01:30:00", 105],
            ["8/15/2019 01:35:00", 80],
            ["8/15/2019 01:40:00", 44],
            ["8/15/2019 01:45:00", 43],
            ["8/15/2019 01:50:00", 50],
            ["8/15/2019 01:55:00", 52],
            ["8/16/2019 02:00:00", 108],
        ],
        dtype=object,
    )
