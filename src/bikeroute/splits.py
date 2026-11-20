"""Split the segment table into training and test sets"""

from __future__ import annotations

import pandas as pd

from . import schema


def split_by_neighborhood(
    table: pd.DataFrame, holdout_neighborhoods: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hold out entire neighborhoods for testing:

    Neighboring streets look alike and share labels, so a random split would
    score well by memorizing streets next to ones it saw in training.

    Returns (training rows, test rows).
    """
    if not holdout_neighborhoods:
        raise ValueError("Choose at least one neighborhood in data.holdout_neighborhoods")
    if schema.NEIGHBORHOOD not in table.columns:
        raise KeyError(f"Segment table needs a '{schema.NEIGHBORHOOD}' column to split by")

    held_out = table[schema.NEIGHBORHOOD].isin(holdout_neighborhoods)
    return table[~held_out].reset_index(drop=True), table[held_out].reset_index(drop=True)
