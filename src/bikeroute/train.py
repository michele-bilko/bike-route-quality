"""Training and evaluation
Run with:  python -m bikeroute.train --config configs/default.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import torch
import yaml
from torch.utils.data import DataLoader

from .dataset import SegmentDataset
from .losses import combined_loss
from .model import TwoBranchQualityModel
from .splits import split_by_neighborhood


def train_one_epoch(model, loader, optimizer, device, stress_weight=1.0, quality_weight=0.5) -> dict:
    """One pass over training data --> returns average losses"""
    model.train()
    totals = {"loss": 0.0, "stress_loss": 0.0, "quality_loss": 0.0}
    batches = 0
    for batch in loader:
        optimizer.zero_grad()
        outputs = model(batch["aerial"].to(device), batch["street"].to(device))
        loss, parts = combined_loss(
            outputs, batch["stress"].to(device), batch["quality"].to(device),
            stress_weight, quality_weight,
        )
        loss.backward()
        optimizer.step()
        totals["loss"] += loss.item()
        totals["stress_loss"] += parts["stress_loss"]
        totals["quality_loss"] += parts["quality_loss"]
        batches += 1
    return {name: value / max(batches, 1) for name, value in totals.items()}


@torch.no_grad()
def evaluate(model, loader, device) -> dict:
    """Stress level accuracy measured on held out data 

    TODO: add macro F1 (balance precision and recall across all four levels),
    accuracy can hide poor results on rare levels, need to add the comparison
    against tag only baseline.
    """
    model.eval()
    correct = 0
    count = 0
    for batch in loader:
        outputs = model(batch["aerial"].to(device), batch["street"].to(device))
        predicted = outputs["stress_logits"].argmax(dim=1).cpu()
        correct += (predicted == batch["stress"]).sum().item()
        count += len(predicted)
    return {"accuracy": correct / max(count, 1)}


def main(config_path: str) -> None:
    config = yaml.safe_load(Path(config_path).read_text())
    data, model_config, training = config["data"], config["model"], config["training"]
    torch.manual_seed(training["seed"])

    table = pd.read_csv(data["segments_table"])
    train_table, test_table = split_by_neighborhood(table, data["holdout_neighborhoods"])
    train_loader = DataLoader(
        SegmentDataset(train_table, data["image_root"], data["image_size"]),
        batch_size=training["batch_size"], shuffle=True,
    )
    test_loader = DataLoader(
        SegmentDataset(test_table, data["image_root"], data["image_size"]),
        batch_size=training["batch_size"],
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = TwoBranchQualityModel(
        backbone=model_config["backbone"],
        pretrained=model_config["pretrained"],
        num_stress_levels=model_config["num_stress_levels"],
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=training["learning_rate"])

    for epoch in range(1, training["epochs"] + 1):
        train_stats = train_one_epoch(
            model, train_loader, optimizer, device,
            training["stress_loss_weight"], training["quality_loss_weight"],
        )
        test_stats = evaluate(model, test_loader, device)
        print(f"epoch {epoch}: train loss {train_stats['loss']:.4f}, "
              f"held-out accuracy {test_stats['accuracy']:.3f}")

    output_dir = Path(training["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), output_dir / "model.pt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/default.yaml")
    main(parser.parse_args().config)
