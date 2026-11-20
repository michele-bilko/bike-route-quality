import pytest

from bikeroute.splits import split_by_neighborhood


def test_holds_out_whole_neighborhoods(synthetic_table):
    table, _ = synthetic_table
    train, test = split_by_neighborhood(table, ["B"])
    assert set(train["neighborhood"]) == {"A"}
    assert set(test["neighborhood"]) == {"B"}
    assert len(train) + len(test) == len(table)


def test_requires_a_holdout_choice(synthetic_table):
    table, _ = synthetic_table
    with pytest.raises(ValueError):
        split_by_neighborhood(table, [])
