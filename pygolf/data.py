import pandas as pd
import numpy as np


class Courses:
    """
    Class to load and manage course data from an Excel file.
    """

    # The columns for the "Courses" sheet in the Excel file
    _COURSES_COLUMNS = {
        "Course Code": pd.StringDtype(),
        "Course Name": pd.StringDtype(),
    }

    # The columns for each holes sheet in the Excel file
    _HOLES_COLUMNS = {
        "Hole": pd.Int64Dtype(),
        "Yardage": pd.Int64Dtype(),
        "Par": pd.Int64Dtype(),
        "Handicap": pd.Int64Dtype(),
    }

    def __init__(self, file_path: str):
        self.file_path = file_path

        self._load_courses()
        self._load_holes()

    def _load_courses(self):
        """
        Load the "Courses" sheet from the Excel file.
        """
        self.courses = pd.read_excel(
            self.file_path, "Courses", dtype=Courses._COURSES_COLUMNS
        ).set_index("Course Code")

    def _load_holes(self):
        """
        Load all the course holes sheets from the Excel file.
        """
        self.holes = pd.concat(
            [
                self._load_holes_sheet(course_code)
                for course_code in self.courses.index
            ],
            ignore_index=True,
        ).set_index(["Course Code", "Hole"])

    def _load_holes_sheet(self, course_code: str) -> pd.DataFrame:
        """
        Load a single course's holes data from the Excel file.
        """
        holes_sheet = pd.read_excel(
            self.file_path, course_code, dtype=Courses._HOLES_COLUMNS
        )

        # We need to associate holes with their course code since we
        # concatenate all holes from different courses into a single DataFrame.
        holes_sheet["Course Code"] = course_code

        return holes_sheet


class Rounds:
    """
    Class to load and manage round scorecard data from an Excel file.
    """

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

    def __init__(self, rounds_path: str, courses_path: str, derived_data: bool = False):
        self.rounds_path = rounds_path
        self.courses_path = courses_path

        self.courses = Courses(self.courses_path)

        self._load_rounds()
        self._load_scorecards()

        if derived_data:
            self._outcome()
            self._gir()
            self._shots_to_green()
            self._non_tee_fairway_attempts()

    def _load_rounds(self):
        """
        Load the "Rounds" sheet from the Excel file.
        """
        self.rounds = pd.read_excel(
            self.rounds_path,
            "Rounds",
            dtype=Rounds._ROUNDS_COLUMNS,
            parse_dates=["Date"],
        )

    def _load_scorecards(self):
        """
        Load all the scorecard sheets from the Excel file.
        """
        self.scorecards = pd.concat(
            [
                self._load_scorecard_sheet(row["Round Code"], row["Course Code"])
                for _, row in self.rounds.iterrows()
            ],
            ignore_index=True,
        )

        # Merge with course data to get the course name and other details
        self.scorecards = pd.merge(
            self.scorecards,
            self.courses.holes.reset_index(),
            "left",
            ["Course Code", "Hole"],
        ).set_index(["Round Code", "Hole"])

    def _load_scorecard_sheet(self, round_code: str, course_code: str) -> pd.DataFrame:
        """
        Load a round's scorecard data from the Excel file.
        """
        scorecard: pd.DataFrame = pd.read_excel(
            self.rounds_path,
            round_code,
            names=Rounds._SCORECARD_COLUMNS.keys(),
            dtype=Rounds._SCORECARD_COLUMNS,
        )

        # We need to associate the scorecard with its round code and course code
        scorecard["Round Code"] = round_code
        scorecard["Course Code"] = course_code

        # Clean the Tee Fairway Hit column (convert to boolean)
        scorecard["TFH"] = (
            scorecard["TFH"].map({"Yes": True, "No": False}).astype(pd.BooleanDtype())
        )

        return scorecard

    def _outcome(self) -> pd.Series:
        """
        Calculate the term for each hole based on the score and par.
        """
        # Outcome masks
        ace = self.scorecards["Score"] == 1
        condor = self.scorecards["Score"] == self.scorecards["Par"] - 3
        eagle = self.scorecards["Score"] == self.scorecards["Par"] - 2
        birdie = self.scorecards["Score"] == self.scorecards["Par"] - 1
        par = self.scorecards["Score"] == self.scorecards["Par"]
        bogey = self.scorecards["Score"] == self.scorecards["Par"] + 1
        double_bogey = self.scorecards["Score"] == self.scorecards["Par"] + 2
        triple_bogey = self.scorecards["Score"] == self.scorecards["Par"] + 3
        blowup = self.scorecards["Score"] >= self.scorecards["Par"] + 4

        # Create the outcomes series
        outcomes = np.select(
            [
                ace,
                condor,
                eagle,
                birdie,
                par,
                bogey,
                double_bogey,
                triple_bogey,
                blowup,
            ],
            [
                "Ace",
                "Condor",
                "Eagle",
                "Birdie",
                "Par",
                "Bogey",
                "Double Bogey",
                "Triple Bogey",
                "+4 or worse",
            ],
            default="Unknown",
        )

        self.scorecards["Outcome"] = outcomes

    def _gir(self) -> pd.Series:
        """
        Calculate the Greens in Regulation (GIR) for each hole.
        """
        self.scorecards["GIR"] = (
            self.scorecards["Score"] - self.scorecards["Putts"]
            <= self.scorecards["Par"] - 2
        )

    def _shots_to_green(self):
        """
        Calculate the number of shots to reach the green for each hole.
        """
        self.scorecards["STG"] = self.scorecards["Score"] - self.scorecards["Putts"]

    def _non_tee_fairway_attempts(self):
        """
        Calculate the non-tee fairway attempts for each hole.
        """
        self.scorecards["NTFA"] = (
            self.scorecards["Score"]
            - self.scorecards["Putts"]
            - self.scorecards["Chips"]
            - 1
        )
