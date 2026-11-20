import pytest

torch = pytest.importorskip("torch")

from bikeroute.dataset import SegmentDataset  # noqa: E402


def test_item_shapes_and_labels(synthetic_table):
    table, root = synthetic_table
    dataset = SegmentDataset(table, root, image_size=64)
    assert len(dataset) == 6
    item = dataset[1]
    assert item["aerial"].shape == (3, 64, 64)
    assert item["street"].shape == (3, 64, 64)
    assert item["stress"].item() == 1  # stress level 2 becomes class 1
    assert torch.isnan(item["quality"])  # odd rows have no quality score


def test_missing_street_photo_gives_blank_image(synthetic_table):
    table, root = synthetic_table
    table.loc[0, "street_path"] = ""
    item = SegmentDataset(table, root, image_size=32)[0]
    assert item["street"].abs().sum().item() == 0


def test_rejects_out_of_range_stress_level(synthetic_table):
    table, root = synthetic_table
    table.loc[0, "stress_level"] = 5
    with pytest.raises(ValueError):
        SegmentDataset(table, root)


def test_rejects_missing_required_column(synthetic_table):
    table, root = synthetic_table
    with pytest.raises(KeyError):
        SegmentDataset(table.drop(columns=["aerial_path"]), root)
