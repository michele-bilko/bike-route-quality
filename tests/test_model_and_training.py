import pytest

torch = pytest.importorskip("torch")

from torch.utils.data import DataLoader  # noqa: E402

from bikeroute.dataset import SegmentDataset  # noqa: E402
from bikeroute.losses import combined_loss  # noqa: E402
from bikeroute.model import TwoBranchQualityModel  # noqa: E402
from bikeroute.train import evaluate, train_one_epoch  # noqa: E402


def small_model():
    # resnet18 without pretrained weights keeps tests fast and offline
    return TwoBranchQualityModel(backbone="resnet18", pretrained=False)


def test_forward_output_shapes():
    outputs = small_model()(torch.randn(2, 3, 64, 64), torch.randn(2, 3, 64, 64))
    assert outputs["stress_logits"].shape == (2, 4)
    assert outputs["quality"].shape == (2,)


def test_loss_ignores_rows_without_a_quality_score():
    outputs = {"stress_logits": torch.randn(3, 4), "quality": torch.rand(3)}
    stress = torch.tensor([0, 1, 2])
    nan = float("nan")
    total, parts = combined_loss(outputs, stress, torch.tensor([nan, nan, nan]))
    assert torch.isfinite(total) and parts["quality_loss"] == 0.0
    total, parts = combined_loss(outputs, stress, torch.tensor([0.5, nan, 0.2]))
    assert torch.isfinite(total) and parts["quality_loss"] > 0.0


def test_one_training_epoch_and_evaluation_run(synthetic_table):
    table, root = synthetic_table
    loader = DataLoader(SegmentDataset(table, root, image_size=64), batch_size=3)
    model = small_model()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    stats = train_one_epoch(model, loader, optimizer, "cpu")
    assert stats["loss"] > 0

    accuracy = evaluate(model, loader, "cpu")["accuracy"]
    assert 0.0 <= accuracy <= 1.0
