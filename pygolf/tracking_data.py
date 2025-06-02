import pandas as pd
from pygolf import golf_stats


class _CourseData:
    """
    Class to load and manage course data from an Excel file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        # Get the course codes and names
        courses = pd.read_excel(
            self.file_path,
            "Courses",
            dtype={
                "Course Code": pd.StringDtype(),
                "Course Name": pd.StringDtype(),
            },
        )

        # Concatenate all course information into a single DataFrame
        self._courses = pd.concat(
            [self._get_course(row["Course Code"]) for _, row in courses.iterrows()],
            ignore_index=True,
        )
        self._courses = self._courses.set_index(["Course Code", "Hole"])

    def _get_course(self, course_code: str) -> pd.DataFrame:
        """
        Load a course's data from the Excel file.
        """
        course = pd.read_excel(
            self.file_path,
            course_code,
            dtype={
                "Hole": pd.Int64Dtype(),
                "Yardage": pd.Int64Dtype(),
                "Par": pd.Int64Dtype(),
                "Handicap": pd.Int64Dtype(),
            },
        )
        course["Course Code"] = course_code

        return course

    def get(self) -> pd.DataFrame:
        """
        Returns the course data as a DataFrame.
        """
        return self._courses


class _ScorecardData:
    """
    Class to load and manage round scorecard data from an Excel file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        # Get the round information
        rounds = pd.read_excel(
            self.file_path,
            "Rounds",
            dtype={
                "Round Code": pd.StringDtype(),
                "Course Code": pd.StringDtype(),
                "Date": pd.StringDtype(),
            },
            parse_dates=["Date"],
        )

        # Concatenate all scorecards into a single DataFrame
        self._scorecards = pd.concat(
            [
                self._get_scorecard(row["Round Code"], row["Course Code"])
                for _, row in rounds.iterrows()
            ],
            ignore_index=True,
        )
        self._scorecards = self._scorecards.set_index(["Round Code", "Hole"])

    def _get_scorecard(self, round_code: str, course_code: str) -> pd.DataFrame:
        """
        Load a round's scorecard data from the Excel file.
        """
        scorecard = pd.read_excel(
            self.file_path,
            round_code,
            names=[
                "Hole",
                "Score",
                "TFH",  # Tee Fairway Hit
                "NTFH",  # Non-Tee Fairway Hit
                "Chips",
                "Putts",
            ],
            dtype={
                "Hole": pd.Int64Dtype(),
                "Score": pd.Int64Dtype(),
                "TFH": pd.StringDtype(),
                "NTFH": pd.Int64Dtype(),
                "Chips": pd.Int64Dtype(),
                "Putts": pd.Int64Dtype(),
            },
        )
        scorecard["Round Code"] = round_code
        scorecard["Course Code"] = course_code

        # Clean the Tee Fairway column
        scorecard["TFH"] = (
            scorecard["TFH"].map({"Yes": True, "No": False}).astype(pd.BooleanDtype())
        )

        return scorecard

    def get(self) -> pd.DataFrame:
        """
        Returns the scorecard data as a DataFrame.
        """
        return self._scorecards


class TrackerData:
    """
    Interface class to load and manage tracking data from the Excel files.
    """

    def __init__(
        self, courses_path: str, scorecards_path: str, derived_data: bool = True
    ):
        """
        Initializes the TrackerData class.

        Parameters
        ----------
            courses_path : str
                Path to the Excel file containing course data.
            scorecards_path : str
                Path to the Excel file containing scorecard data.
            derived_data : bool, optional
                If True, derived data will be calculated and added to the DataFrame.
        """
        self.course_path = courses_path
        self.scorecards_path = scorecards_path

        self._course_data = _CourseData(self.course_path)
        self._scorecard_data = _ScorecardData(self.scorecards_path)

        # Merge the course and scorecard data into a single DataFrame
        self._tracking_data = pd.merge(
            self._scorecard_data.get().reset_index(),
            self._course_data.get().reset_index(),
            on=["Course Code", "Hole"],
            how="left",
        ).set_index(["Round Code", "Hole"])

        if derived_data:
            self._derived_data()

    def get(self) -> pd.DataFrame:
        """
        Returns the tracking data as a DataFrame.
        """
        return self._tracking_data

    def _derived_data(self) -> pd.DataFrame:
        """
        Calculate derived data for the tracking DataFrame.
        """
        self._tracking_data["Outcome"] = golf_stats.outcome(self._tracking_data)
        self._tracking_data["GIR"] = golf_stats.gir(self._tracking_data)
        self._tracking_data["STG"] = golf_stats.shots_to_green(self._tracking_data)
        self._tracking_data["NTFA"] = golf_stats.non_tee_fairway_attempts(self._tracking_data)
