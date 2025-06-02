import pandas as pd
import numpy as np


def hole_term(tracking_data: pd.DataFrame) -> pd.Series:
    """
    Calculate the term for each hole based on the score and par.
    """
    # Term masks
    ace = tracking_data["Score"] == 1
    condor = tracking_data["Score"] == tracking_data["Par"] - 3
    eagle = tracking_data["Score"] == tracking_data["Par"] - 2
    birdie = tracking_data["Score"] == tracking_data["Par"] - 1
    par = tracking_data["Score"] == tracking_data["Par"]
    bogey = tracking_data["Score"] == tracking_data["Par"] + 1
    double_bogey = tracking_data["Score"] == tracking_data["Par"] + 2
    triple_bogey = tracking_data["Score"] == tracking_data["Par"] + 3
    blowup = tracking_data["Score"] >= tracking_data["Par"] + 4

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


def gir(tracking_data: pd.DataFrame) -> pd.Series:
    """
    Calculate the Greens in Regulation (GIR) for each hole.
    """
    return tracking_data["Score"] - tracking_data["Putts"] <= tracking_data["Par"] - 2


def shots_to_green(tracking_data: pd.DataFrame) -> pd.Series:
    """
    Calculate the number of shots to reach the green for each hole.
    """
    return tracking_data["Score"] - tracking_data["Putts"]


def fairways(tracking_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the fairway hits and attempts for each hole.
    """
    fairway_hits = tracking_data["Tee Fairway"] + tracking_data["Fairway Hits"]
    fairway_attempts = (
        tracking_data["Score"] - tracking_data["Putts"] - tracking_data["Chips"]
    )

    fairways_df = pd.DataFrame(
        {"Fairway Hits": fairway_hits, "Fairway Attempts": fairway_attempts}
    )

    return fairways_df
