import pygolf
import pandas as pd
from pandas.testing import assert_frame_equal


def test_TrackerData():
    data = pygolf.GolfTracker(
        "test/test_data_files/courses.xlsx",
        "test/test_data_files/rounds.xlsx",
        derived_data=False,
    )

    expected_df = pd.read_parquet("test/test_data_files/expected_holes_df.parquet")

    assert_frame_equal(data.holes_df, expected_df)


def test_TrackerData_derived():
    data = pygolf.GolfTracker(
        "test/test_data_files/courses.xlsx",
        "test/test_data_files/rounds.xlsx",
        derived_data=True,
    )

    expected_df = pd.read_parquet(
        "test/test_data_files/expected_holes_df_derived.parquet"
    )

    assert_frame_equal(data.holes_df, expected_df)
