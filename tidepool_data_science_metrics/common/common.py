import numpy as np


def mean(bg_values, round_val=2):
    """
        Calculate the mean within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Mean
    """
    return round(np.mean(bg_values), round_val)


def avg(bg_values, round_val=2):
    """
        Calculate the average within a set of glucose values

        Arguments:
        values -- numpy array contains a list of bg values.
        round_val -- the number of digits to round the result to.

        Output: Calculated Average
    """
    return round(np.average(bg_values), round_val)


def std_deviation(bg_values, round_val=2):
    """
            Calculate the standard deviation within a set of glucose values

            Arguments:
            values -- numpy array contains a list of bg values.
            round_val -- the number of digits to round the result to.

            Output: Calculated standard deviation
    """
    return round(np.std(bg_values), round_val)