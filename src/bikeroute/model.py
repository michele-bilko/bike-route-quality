"""The model exists as two image encoders feeding one shared prediction head."""

from __future__ import annotations

import torch
import torchvision
from torch import nn


def _make_encoder(backbone: str, pretrained: bool) -> tuple[nn.Module, int]:
    """torchvision ResNet with final classification layer removed"""
    encoder = torchvision.models.get_model(backbone, weights="DEFAULT" if pretrained else None)
    if not hasattr(encoder, "fc"):
        raise ValueError(f"'{backbone}' is not a ResNet")
    feature_size = encoder.fc.in_features
    encoder.fc = nn.Identity()
    return encoder, feature_size


class TwoBranchQualityModel(nn.Module):
    """Predicts cycling comfort for a street segment from two views of it

    The aerial branch sees layout (lane width, buffer space). 
    The street level branch sees what aerial images miss (physical barriers, parked cars, surface condition)
    Their features are joined and feed two outputs:

      stress_logits-->scores for each stress level (1 comfortable to 4 stressful)
      quality-->a continuous quality score
    """

    def __init__(
        self,
        backbone: str = "resnet50",
        pretrained: bool = True,
        num_stress_levels: int = 4,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.aerial_encoder, feature_size = _make_encoder(backbone, pretrained)
        self.street_encoder, _ = _make_encoder(backbone, pretrained)
        self.shared = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(2 * feature_size, 256),
            nn.ReLU(),
        )
        self.stress_head = nn.Linear(256, num_stress_levels)
        self.quality_head = nn.Linear(256, 1)

    def forward(self, aerial: torch.Tensor, street: torch.Tensor) -> dict[str, torch.Tensor]:
        features = torch.cat([self.aerial_encoder(aerial), self.street_encoder(street)], dim=1)
        hidden = self.shared(features)
        return {
            "stress_logits": self.stress_head(hidden),
            "quality": self.quality_head(hidden).squeeze(-1),
        }
