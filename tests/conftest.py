import pytest
import pandas as pd
import numpy as np
import os
from pathlib import Path


@pytest.fixture
def bg_array(scope="module"):
    return np.genfromtxt(
        f"{Path(__file__).parent.resolve()}/bg_array.csv", delimiter=","
    )


@pytest.fixture
def bg_values__3_values(scope="module"):
    return np.array([[100], [105], [108]])


@pytest.fixture
def get_date_ep_array(scope="module"):
    print("path is : ", os.getcwd())
    df = pd.read_csv(f"{Path(__file__).parent.resolve()}/date_ep_values.csv")
    return df.to_numpy(dtype=object)
