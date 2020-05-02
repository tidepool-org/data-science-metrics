import pytest
from tidepool_data_science_metrics.cgm.cgm import (
    percent_values_by_range,
    cv_of_glucose,
    gmi,
    bgri,
    episodes,
    percent_time_in_range_70_180,
    percent_time_above_250,
    percent_time_below_54,
    percent_time_below_70,
    percent_time_above_180,
)


def test_percent_values_by_range(bg_array):
    percent = percent_values_by_range(bg_array, 100, 0)
    assert 22.0 == percent


def test_invalid_lower_number(bg_array):
    with pytest.raises(Exception) as excinfo:
        percent_values_by_range(bg_array, -1, 0)
    assert "lower and upper thresholds must be a non-negative number" in str(
        excinfo.value
    )


def test_invalid_upper_number(bg_array):
    with pytest.raises(Exception) as excinfo:
        percent_values_by_range(bg_array, 0, -1)
    assert "lower and upper thresholds must be a non-negative number" in str(
        excinfo.value
    )


def test_missing_lower_number(bg_array):
    with pytest.raises(TypeError) as excinfo:
        percent_values_by_range(bg_array)
    assert (
        "percent_values_by_range() missing 2 required "
        "positional arguments: "
        "'lower_threshold' and 'upper_threshold'" in str(excinfo.value)
    )


def test_lower_number_higher_than_upper_number(bg_array):
    with pytest.raises(Exception) as excinfo:
        percent_values_by_range(bg_array, 100, 20)
    assert "lower threshold is higher than the " "upper threshold." in str(
        excinfo.value
    )


def test_gmi(bg_array):
    gmi_value = gmi(bg_array)
    assert gmi_value == 5.43


def test_gmi_round(bg_array):
    gmi_value = gmi(bg_array, 3)
    assert gmi_value == 5.432


def test_cv_of_glucose(bg_array):
    std = cv_of_glucose(bg_array)
    assert std == 24.9


def test_cv_of_glucose_round(bg_array):
    std = cv_of_glucose(bg_array, 3)
    assert std == 24.891


def test_get_bgri(bg_array):
    LBGI, HBGI, BGRI = bgri(bg_array)
    assert BGRI == 3.54
    assert HBGI == 0.3
    assert LBGI == 3.24


def test_get_bgri_round(bg_array):
    LBGI, HBGI, BGRI = bgri(bg_array, 3)
    assert BGRI == 3.543
    assert HBGI == 0.303
    assert LBGI == 3.24


def test_get_episodes_3_consecutive(get_date_ep_array):
    pd_values = get_date_ep_array
    std = episodes(pd_values, 55, 3)
    assert std == 2


def test_get_episodes_4_consecutive(get_date_ep_array):
    pd_values = get_date_ep_array
    std = episodes(pd_values, 55, 4)
    assert std == 1


def test_episodes_nonconsecutive(get_date_ep_array):
    pd_values = get_date_ep_array
    std = episodes(pd_values, 55, 6)
    assert std == 0


def test_percent_time_in_range_70_180(bg_array):
    percent = percent_time_in_range_70_180(bg_array)
    assert percent == 96.0


def test_percent_time_in_range_70_180_round(bg_array):
    percent = percent_time_in_range_70_180(bg_array, round_val=0)
    assert percent == 96


def test_percent_time_above_180(bg_array):
    percent = percent_time_above_180(bg_array)
    assert 2.0 == percent


def test_percent_time_above_180_round(bg_array):
    percent = percent_time_above_180(bg_array, round_val=0)
    assert 2 == percent


def test_percent_time_below_70(bg_array):
    percent = percent_time_below_70(bg_array)
    assert percent == 3.0


def test_percent_time_below_70_round(bg_array):
    percent = percent_time_below_70(bg_array, round_val=0)
    assert percent == 3


def test_percent_time_below_54(bg_array):
    percent = percent_time_below_54(bg_array)
    assert percent == 1.0


def test_percent_time_below_54_round(bg_array):
    percent = percent_time_below_54(bg_array, round_val=0)
    assert percent == 1


def test_percent_time_above_250(bg_array):
    percent = percent_time_above_250(bg_array)
    assert percent == 1.0


def test_percent_time_above_250(bg_array):
    percent = percent_time_above_250(bg_array, round_val=0)
    assert percent == 1
