import pandas as pd


class _CourseData:
    """
    Class to load and manage course data from an Excel file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

        # Get the course codes and names
        courses = pd.read_excel(self.file_path, "Courses")

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
        course = pd.read_excel(self.file_path, course_code)
        course["Course Code"] = course_code

        # Enforce types
        course["Hole"] = course["Hole"].astype(int)
        course["Yardage"] = course["Yardage"].astype(int)
        course["Par"] = course["Par"].astype(int)
        course["Handicap"] = course["Handicap"].astype(int)

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
        rounds = pd.read_excel(self.file_path, "Rounds")

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
        scorecard = pd.read_excel(self.file_path, round_code)
        scorecard["Round Code"] = round_code
        scorecard["Course Code"] = course_code

        # Clean the tee fairway column
        scorecard["Tee Fairway"] = scorecard["Tee Fairway"].map({"Yes": 1.0, "No": 0.0})

        # Enforce types
        scorecard["Hole"] = scorecard["Hole"].astype(int)
        scorecard["Score"] = scorecard["Score"].astype(int)
        scorecard["Tee Fairway"] = scorecard["Tee Fairway"].astype(float)
        scorecard["Fairway Hits"] = scorecard["Fairway Hits"].astype(float)
        scorecard["Chips"] = scorecard["Chips"].astype(float)
        scorecard["Putts"] = scorecard["Putts"].astype(float)

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

    def __init__(self, courses_path: str, scorecards_path: str):
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

    def get(self) -> pd.DataFrame:
        """
        Returns the tracking data as a DataFrame.
        """
        return self._tracking_data
