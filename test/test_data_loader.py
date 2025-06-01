import golftrack
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


def test_TrackerData():
    data = golftrack.TrackerData("test/test_data_loader.xlsx")

    expected_courses = pd.DataFrame(
        {
            "Course Name": {
                "CGC-B": "Charlevoix Golf Club Blue",
                "CGC-W": "Charlevoix Golf Club White",
                "CGC-R": "Charlevoix Golf Club Red",
                "CGC-Y": "Charlevoix Golf Club Yellow",
            },
            "Hole 1": {"CGC-B": 278, "CGC-W": 256, "CGC-R": 230, "CGC-Y": 136},
            "Hole 2": {"CGC-B": 402, "CGC-W": 393, "CGC-R": 312, "CGC-Y": 143},
            "Hole 3": {"CGC-B": 184, "CGC-W": 170, "CGC-R": 109, "CGC-Y": 68},
            "Hole 4": {"CGC-B": 318, "CGC-W": 272, "CGC-R": 254, "CGC-Y": 147},
            "Hole 5": {"CGC-B": 363, "CGC-W": 333, "CGC-R": 290, "CGC-Y": 162},
            "Hole 6": {"CGC-B": 453, "CGC-W": 439, "CGC-R": 312, "CGC-Y": 225},
            "Hole 7": {"CGC-B": 193, "CGC-W": 165, "CGC-R": 120, "CGC-Y": 70},
            "Hole 8": {"CGC-B": 358, "CGC-W": 343, "CGC-R": 294, "CGC-Y": 168},
            "Hole 9": {"CGC-B": 466, "CGC-W": 451, "CGC-R": 360, "CGC-Y": 200},
            "Hole 10": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 11": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 12": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 13": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 14": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 15": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 16": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 17": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
            "Hole 18": {
                "CGC-B": np.nan,
                "CGC-W": np.nan,
                "CGC-R": np.nan,
                "CGC-Y": np.nan,
            },
        }
    )
    expected_courses.index.name = "Course Code"

    assert_frame_equal(data.courses, expected_courses)

    expected_scorecard = pd.DataFrame(
        {
            "Score": {1: 6, 2: 7, 3: 4, 4: 9, 5: 5, 6: 6, 7: 6, 8: 6, 9: 9},
            "Fairway Hits": {
                1: np.nan,
                2: np.nan,
                3: np.nan,
                4: np.nan,
                5: np.nan,
                6: np.nan,
                7: np.nan,
                8: np.nan,
                9: np.nan,
            },
            "Chips": {
                1: np.nan,
                2: np.nan,
                3: np.nan,
                4: np.nan,
                5: np.nan,
                6: np.nan,
                7: np.nan,
                8: np.nan,
                9: np.nan,
            },
            "Putts": {1: 3, 2: 3, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 2},
            "Yardage": {
                1: 256,
                2: 393,
                3: 170,
                4: 272,
                5: 333,
                6: 439,
                7: 165,
                8: 343,
                9: 451,
            },
        }
    )
    expected_scorecard.index.name = "Hole"
    expected_scorecard["Yardage"] = expected_scorecard["Yardage"].astype(object)

    assert_frame_equal(
        data.rounds.loc["CGC-W-05312025", "Scorecard"], expected_scorecard
    )
