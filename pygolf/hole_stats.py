import pandas as pd
import numpy as np


def outcome(holes_df: pd.DataFrame) -> pd.Series:
    """
    Calculate the term for each hole based on the score and par.
    """
    # Term masks
    ace = holes_df["Score"] == 1
    condor = holes_df["Score"] == holes_df["Par"] - 3
    eagle = holes_df["Score"] == holes_df["Par"] - 2
    birdie = holes_df["Score"] == holes_df["Par"] - 1
    par = holes_df["Score"] == holes_df["Par"]
    bogey = holes_df["Score"] == holes_df["Par"] + 1
    double_bogey = holes_df["Score"] == holes_df["Par"] + 2
    triple_bogey = holes_df["Score"] == holes_df["Par"] + 3
    blowup = holes_df["Score"] >= holes_df["Par"] + 4

    # Create the terms series
    terms = np.select(
        [ace, condor, eagle, birdie, par, bogey, double_bogey, triple_bogey, blowup],
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

    return terms


def gir(holes_df: pd.DataFrame) -> pd.Series:
    """
    Calculate the Greens in Regulation (GIR) for each hole.
    """
    return holes_df["Score"] - holes_df["Putts"] <= holes_df["Par"] - 2


def shots_to_green(holes_df: pd.DataFrame) -> pd.Series:
    """
    Calculate the number of shots to reach the green for each hole.
    """
    return holes_df["Score"] - holes_df["Putts"]


def non_tee_fairway_attempts(holes_df: pd.DataFrame) -> pd.Series:
    """
    Calculate the non-tee fairway attempts for each hole.
    """
    return holes_df["Score"] - holes_df["Putts"] - holes_df["Chips"] - 1
