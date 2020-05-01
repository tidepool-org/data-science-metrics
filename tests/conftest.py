import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def bg_array(scope="module"):
    return np.genfromtxt("../bg_array.csv", delimiter=",")


@pytest.fixture
def bg_values__3_values(scope="module"):
    return np.array([[100], [105], [108]])


@pytest.fixture
def get_date_ep_array(scope="module"):
    df = pd.read_csv("../date_ep_values.csv")
    return df.to_numpy(dtype=object)
