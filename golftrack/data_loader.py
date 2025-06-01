import pandas as pd


class TrackerData:
    def __init__(self, file_path: str):
        self.file_path = file_path

        self._read_courses()
        self._read_rounds()
        self._read_scorecards()

    def _read_courses(self):
        self.courses = pd.read_excel(self.file_path, "Courses")
        self.courses = self.courses.set_index("Course Code")

    def _read_rounds(self):
        self.rounds = pd.read_excel(self.file_path, "Rounds")
        self.rounds = pd.merge(
            self.rounds,
            self.courses[["Course Name"]],
            "left",
            "Course Code",
        )
        self.rounds = self.rounds.set_index("Sheet Name")

    def _read_scorecards(self):
        scorecards = [
            self._read_scorecard(row["Course Code"], sheet_name)
            for sheet_name, row in self.rounds.iterrows()
        ]
        self.rounds["Scorecard"] = scorecards

    def _read_scorecard(self, course_code: str, sheet_name: str) -> pd.DataFrame:
        # Get the course yardage information
        yardage = self.courses.loc[course_code]
        yardage = yardage.drop("Course Name")
        yardage.name = "Yardage"
        yardage.index.name = "Hole"
        yardage.index = yardage.index.str[5:].astype(int)

        # Read the scorecard and merge the yardage information
        scorecard = pd.read_excel(self.file_path, sheet_name)
        scorecard = scorecard.set_index("Hole")
        scorecard = pd.merge(
            scorecard, yardage, left_index=True, right_index=True, how="left"
        )

        return scorecard
