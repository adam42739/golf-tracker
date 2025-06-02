import pygolf
import pandas as pd
from pandas.testing import assert_frame_equal


def test_TrackerData():
    data = pygolf.TrackerData(
        "test/test_data/courses.xlsx",
        "test/test_data/scorecards.xlsx",
        derived_data=False,
    )

    expected_df = pd.read_parquet("test/test_data/expected_tracking_data.parquet")

    assert_frame_equal(data.get(), expected_df)


def test_TrackerData_derived():
    data = pygolf.TrackerData(
        "test/test_data/courses.xlsx",
        "test/test_data/scorecards.xlsx",
        derived_data=True,
    )

    expected_df = pd.read_parquet(
        "test/test_data/expected_tracking_data_derived.parquet"
    )

    assert_frame_equal(data.get(), expected_df)
