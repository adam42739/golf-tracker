import golftrack
import pandas as pd
from pandas.testing import assert_frame_equal


def test_TrackerData():
    data = golftrack.TrackerData(
        "test/test_data/courses.xlsx", "test/test_data/scorecards.xlsx"
    )

    expected_df = pd.read_parquet(
        "test/test_data/expected_tracking_data.parquet"
    )

    assert_frame_equal(data.get(), expected_df)
