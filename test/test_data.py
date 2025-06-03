import pygolf
import pandas as pd
from pandas.testing import assert_frame_equal


def test_Rounds():
    data = pygolf.Rounds(
        "test/test_data_files/rounds.xlsx",
        "test/test_data_files/courses.xlsx",
        derived_data=False,
    )

    expected_df = pd.read_parquet("test/test_data_files/expected_rounds.parquet")

    assert_frame_equal(data.scorecards, expected_df)


def test_Rounds_derived():
    data = pygolf.Rounds(
        "test/test_data_files/rounds.xlsx",
        "test/test_data_files/courses.xlsx",
        derived_data=True,
    )

    expected_df = pd.read_parquet(
        "test/test_data_files/expected_rounds_derived.parquet"
    )

    assert_frame_equal(data.scorecards, expected_df)
