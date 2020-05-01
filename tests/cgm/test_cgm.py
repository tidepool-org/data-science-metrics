import pytest
from tidepool_data_science_metrics.cgm.cgm import (
    percent_values_by_range,
    cv_of_glucose,
    gmi,
    bgri,
    episodes,
)


def test_calculation(bg_array):
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
    assert gmi_value == 5.38


def test_gmi_round(bg_array):
    gmi_value = gmi(bg_array, 3)
    assert gmi_value == 5.379


def test_cv_of_glucose(bg_array):
    std = cv_of_glucose(bg_array)
    assert std == 13.76


def test_cv_of_glucose_round(bg_array):
    std = cv_of_glucose(bg_array, 3)
    assert std == 13.764


def test_get_bgri(bg_array):
    LBGI, HBGI, BGRI = bgri(bg_array)
    assert BGRI == 3.25
    assert HBGI == 0.0
    assert LBGI == 3.25


def test_get_bgri_round(bg_array):
    LBGI, HBGI, BGRI = bgri(bg_array, 3)
    assert BGRI == 3.245
    assert HBGI == 0.0
    assert LBGI == 3.245


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
