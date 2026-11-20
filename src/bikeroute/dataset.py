"""Turn the segment table into training examples"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset

from . import schema

# stats from ImageNet images that the pretrained networks were trained on
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


class SegmentDataset(Dataset):
    """One example per street segment: an aerial crop and a street level photo

    Each item is a dictionary with:
      segment_id-->text identifier
      aerial-->float tensor, 3 x size x size
      street-->float tensor, 3 x size x size (all zeros when the photo is missing)
      stress-->integer class 0 to 3 (stress level minus one)
      quality-->float score between 0-1, or NaN when the row has no quality score
    """

    def __init__(self, table: pd.DataFrame, root: str | Path, image_size: int = 224):
        for column in (schema.SEGMENT_ID, schema.AERIAL_PATH, schema.STRESS_LEVEL):
            if column not in table.columns:
                raise KeyError(f"Segment table is missing required column '{column}'")
        levels = table[schema.STRESS_LEVEL].astype(int)
        if not levels.between(1, schema.NUM_STRESS_LEVELS).all():
            raise ValueError(f"'{schema.STRESS_LEVEL}' must be between 1 and {schema.NUM_STRESS_LEVELS}")

        self.table = table.reset_index(drop=True)
        self.root = Path(root)
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.table)

    def __getitem__(self, index: int) -> dict:
        row = self.table.iloc[index]
        quality = row.get(schema.QUALITY_SCORE, float("nan"))
        return {
            "segment_id": str(row[schema.SEGMENT_ID]),
            "aerial": self._load_image(row[schema.AERIAL_PATH]),
            # TODO: street level coverage is uneven, so many segments have no photo
            # A blank image is a placeholder: later, tell the model which inputs are missing
            "street": self._load_image(row.get(schema.STREET_PATH)),
            "stress": torch.tensor(int(row[schema.STRESS_LEVEL]) - 1, dtype=torch.long),
            "quality": torch.tensor(float(quality), dtype=torch.float32),
        }

    def _load_image(self, relative_path) -> torch.Tensor:
        size = self.image_size
        if not isinstance(relative_path, str) or not relative_path:
            return torch.zeros(3, size, size)
        image = Image.open(self.root / relative_path).convert("RGB").resize((size, size))
        array = np.asarray(image, dtype=np.float32) / 255.0
        tensor = torch.from_numpy(array).permute(2, 0, 1)
        mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
        std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
        return (tensor - mean) / std
