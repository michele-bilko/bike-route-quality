"""Training objective"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def combined_loss(
    outputs: dict[str, torch.Tensor],
    stress: torch.Tensor,
    quality: torch.Tensor,
    stress_weight: float = 1.0,
    quality_weight: float = 0.5,
) -> tuple[torch.Tensor, dict[str, float]]:
    """Stress level classification loss plus quality score regression loss

    Many rows have no quality score (NaN), so the regression term uses only rows
    that have one. A batch with none contributes zero to that term.
    """
    stress_loss = F.cross_entropy(outputs["stress_logits"], stress)

    has_score = ~torch.isnan(quality)
    if has_score.any():
        quality_loss = F.smooth_l1_loss(outputs["quality"][has_score], quality[has_score])
    else:
        quality_loss = outputs["quality"].sum() * 0.0

    total = stress_weight * stress_loss + quality_weight * quality_loss
    parts = {"stress_loss": stress_loss.item(), "quality_loss": quality_loss.item()}
    return total, parts
