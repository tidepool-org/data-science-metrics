import pytest
import numpy as np
from tidepool_data_science_metrics.cgm.cgm import (
    percent_values_by_range,
    gmi,
    blood_glucose_risk_index,
    episodes,
    percent_values_ge_70_le_180,
    percent_time_above_250,
    percent_time_below_54,
    percent_time_below_70,
    percent_time_above_180,
    _validate_bg,
)


def test_percent_values_by_range():
    bg_array = np.array([40, 70, 180, 400])
    percent = percent_values_by_range(bg_array, 0, 140)
    assert percent == 50.0


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
        "'lower_bound' and 'upper_bound'" in str(excinfo.value)
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


def test_gmi_warning_low_and_high(bg_array_low_high):
    with pytest.warns(UserWarning) as record:
        gmi_value = gmi(bg_array_low_high)

    # check that only one warning was raised
    assert len(record) == 2
    # check that the message matches
    assert (
        record[0].message.args[0]
        == "Some values in the passed in array had glucose values less than 38."
    )

    # check that the message matches
    assert (
        record[1].message.args[0]
        == "Some values in the passed in array had glucose values greater than 402."
    )


def test_gmi_warning_low(bg_array_low):
    with pytest.warns(UserWarning) as record:
        gmi_value = _validate_bg(bg_array_low)

    assert len(record) == 1

    assert (
        record[0].message.args[0]
        == "Some values in the passed in array had glucose values less than 38."
    )


def test_gmi_warning_high(bg_array_high):
    with pytest.warns(UserWarning) as record:
        gmi_value = _validate_bg(bg_array_high)

    assert len(record) == 1

    assert (
        record[0].message.args[0]
        == "Some values in the passed in array had glucose values greater than 402."
    )


def test_gmi_round(bg_array):
    gmi_value = gmi(bg_array, 4)
    assert gmi_value == 5.4303


def test_blood_glucose_risk_index(bg_array):

    LBGI, HBGI, BGRI = blood_glucose_risk_index(bg_array)
    assert BGRI == 3.58
    assert HBGI == 0.31
    assert LBGI == 3.27


def test_blood_glucose_risk_index_round(bg_array):
    LBGI, HBGI, BGRI = blood_glucose_risk_index(bg_array, 3)
    assert BGRI == 3.579
    assert HBGI == 0.311
    assert LBGI == 3.267


def test_get_episodes_3_consecutive(get_episodes_array):
    pd_values = get_episodes_array
    std = episodes(pd_values, 55, 3)
    assert std == 2


def test_get_episodes_4_consecutive(get_episodes_array):
    pd_values = get_episodes_array
    std = episodes(pd_values, 55, 4)
    assert std == 1


def test_episodes_nonconsecutive(get_episodes_array):
    pd_values = get_episodes_array
    std = episodes(pd_values, 55, 6)
    assert std == 0


def test_percent_values_ge_70_le_180(bg_array):
    percent = percent_values_ge_70_le_180(bg_array)
    assert percent == 96


def test_percent_values_ge_70_le_180(bg_array):
    percent = percent_values_ge_70_le_180(bg_array, round_to_n_digits=0)
    assert percent == 96


def test_percent_values_ge_70_le_180_around_70():
    bg_array = np.array([69.99999, 70, 70.00001])
    percent = percent_values_ge_70_le_180(bg_array, round_to_n_digits=1)
    assert percent == 66.7


def test_percent_values_ge_70_le_180_around_180():
    bg_array = np.array([70, 179.9999999, 180, 180.0000000001])
    percent = percent_values_ge_70_le_180(bg_array, round_to_n_digits=0)
    assert percent == 75


#
# def test_percent_time_above_180(bg_array):
#     percent = percent_time_above_180(bg_array)
#     typeo = type(percent)
#     assert percent == 2.02
#
#
# def test_percent_time_above_180_round(bg_array):
#     percent = percent_time_above_180(bg_array, round_to_ndigits=0)
#     assert 2 == percent
#
#
# def test_percent_time_below_70(bg_array):
#     percent = percent_time_below_70(bg_array)
#     assert percent == 2.02
#
#
# def test_percent_time_below_70_round(bg_array):
#     percent = percent_time_below_70(bg_array, round_to_ndigits=0)
#     assert percent == 2.0
#
#
# def test_percent_time_below_54(bg_array):
#     percent = percent_time_below_54(bg_array)
#     assert percent == 1.01
#
#
# def test_percent_time_below_54_round(bg_array):
#     percent = percent_time_below_54(bg_array, round_to_ndigits=0)
#     assert percent == 1
#
#
# def test_percent_time_above_250(bg_array):
#     percent = percent_time_above_250(bg_array)
#     assert percent == 1.01
#
#
# def test_percent_time_above_250_round(bg_array):
#     percent = percent_time_above_250(bg_array, round_to_ndigits=0)
#     assert percent == 1
#
#
def test_invalid_lower_less_than_1(bg_array_less_than_one):
    with pytest.raises(Exception) as excinfo:
        percent_values_by_range(bg_array_less_than_one, 0, 1001)
    assert (
        "Some values in the passed in array had glucose values less than 1."
        in str(excinfo.value)
    )


def test_invalid_lower_greater_than_1000(bg_array_greater_than_1000):
    with pytest.raises(Exception) as excinfo:
        percent_values_by_range(bg_array_greater_than_1000, 0, 1001)
    assert (
        "Some values in the passed in array had glucose values greater than 1000."
        in str(excinfo.value)
    )


# def test_percent_time_across_multiple_functions(bg_array):
#     total = (
#         percent_time_below_70(bg_array, round_to_ndigits=0)
#         + percent_values_by_range(bg_array, 69.99, 180.99, round_to_ndigits=0)
#         + percent_time_above_180(bg_array, round_to_ndigits=0)
#     )
#     assert total == 100
