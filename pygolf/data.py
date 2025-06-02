import pandas as pd
from pygolf import stats


# The columns for the "Courses" sheet in the Excel file
_COURSES_COLUMNS = {
    "Course Code": pd.StringDtype(),
    "Course Name": pd.StringDtype(),
}


# The columns for each course description sheet in the Excel file
_COURSE_DESC_COLUMNS = {
    "Hole": pd.Int64Dtype(),
    "Yardage": pd.Int64Dtype(),
    "Par": pd.Int64Dtype(),
    "Handicap": pd.Int64Dtype(),
}


class _Courses:
    """
    Class to load and manage course data from an Excel file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        self._load_courses()
        self._load_desc_all()

    def _load_courses(self):
        """
        Load the "Courses" sheet from the Excel file.
        """
        self.courses = pd.read_excel(self.file_path, "Courses", dtype=_COURSES_COLUMNS)

    def _load_desc_all(self):
        """
        Load all the course description sheets from the Excel file.
        """
        self.descs = pd.concat(
            [
                self._load_desc_single(course_code)
                for course_code in self.courses["Course Code"]
            ],
            ignore_index=True,
        ).set_index(["Course Code", "Hole"])

    def _load_desc_single(self, course_code: str) -> pd.DataFrame:
        """
        Load a course's description data from the Excel file.
        """
        course = pd.read_excel(self.file_path, course_code, dtype=_COURSE_DESC_COLUMNS)
        course["Course Code"] = course_code

        return course


# The columns for the "Rounds" sheet in the Excel file
_ROUNDS_COLUMNS = {
    "Round Code": pd.StringDtype(),
    "Course Code": pd.StringDtype(),
    "Date": pd.StringDtype(),
}


# The columns for each round scorecard sheet in the Excel file
_SCORECARD_COLUMNS = {
    "Hole": pd.Int64Dtype(),
    "Score": pd.Int64Dtype(),
    "TFH": pd.StringDtype(),  # Tee Fairway Hit (Yes/No in the Excel file but converted to BooleanDtype later)
    "NTFH": pd.Int64Dtype(),  # Non-Tee Fairway Hits
    "Chips": pd.Int64Dtype(),
    "Putts": pd.Int64Dtype(),
}


class _Rounds:
    """
    Class to load and manage round scorecard data from an Excel file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        self._load_rounds()
        self._load_scorecard_all()

    def _load_rounds(self):
        """
        Load the "Rounds" sheet from the Excel file.
        """
        self.rounds = pd.read_excel(
            self.file_path, "Rounds", dtype=_ROUNDS_COLUMNS, parse_dates=["Date"]
        )

    def _load_scorecard_all(self):
        """
        Load all the scorecard sheets from the Excel file.
        """
        self.scorecards = pd.concat(
            [
                self._load_scorecard_single(row["Round Code"], row["Course Code"])
                for _, row in self.rounds.iterrows()
            ],
            ignore_index=True,
        ).set_index(["Round Code", "Hole"])

    def _load_scorecard_single(self, round_code: str, course_code: str) -> pd.DataFrame:
        """
        Load a round's scorecard data from the Excel file.
        """
        scorecard: pd.DataFrame = pd.read_excel(
            self.file_path,
            round_code,
            names=_SCORECARD_COLUMNS.keys(),
            dtype=_SCORECARD_COLUMNS,
        )
        scorecard["Round Code"] = round_code
        scorecard["Course Code"] = course_code

        # Clean the Tee Fairway column
        scorecard["TFH"] = (
            scorecard["TFH"].map({"Yes": True, "No": False}).astype(pd.BooleanDtype())
        )

        return scorecard


class GolfTracker:
    """
    Interface class to load and manage golf tracking data from the Excel files.
    """

    def __init__(
        self, courses_path: str, scorecards_path: str, derived_data: bool = True
    ):
        """
        Initializes the GolfTracker class.

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

        self.courses = _Courses(self.course_path)
        self.rounds = _Rounds(self.scorecards_path)

        self._create_tracking_data()

        if derived_data:
            self._derived_data()

    def _create_tracking_data(self):
        """
        Create the tracking DataFrame by merging course and scorecard data.
        """
        self.tracking_data = pd.merge(
            self.rounds.scorecards.reset_index(),
            self.courses.descs.reset_index(),
            on=["Course Code", "Hole"],
            how="left",
        ).set_index(["Round Code", "Hole"])

    def _derived_data(self) -> pd.DataFrame:
        """
        Calculate derived data for the tracking DataFrame.
        """
        self.tracking_data["Outcome"] = stats.outcome(self.tracking_data)
        self.tracking_data["GIR"] = stats.gir(self.tracking_data)
        self.tracking_data["STG"] = stats.shots_to_green(self.tracking_data)
        self.tracking_data["NTFA"] = stats.non_tee_fairway_attempts(self.tracking_data)
