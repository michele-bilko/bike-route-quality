import numpy as np
import pandas as pd
import pytest
from PIL import Image


@pytest.fixture
def synthetic_table(tmp_path):
    """Six fake segments with random images"""
    rng = np.random.default_rng(0)
    rows = []
    for i in range(6):
        for kind in ("aerial", "street"):
            pixels = rng.integers(0, 255, (40, 40, 3), dtype=np.uint8)
            Image.fromarray(pixels).save(tmp_path / f"{kind}_{i}.png")
        rows.append({
            "segment_id": f"s{i}",
            "aerial_path": f"aerial_{i}.png",
            "street_path": f"street_{i}.png",
            "stress_level": 1 + i % 4,
            "quality_score": i / 5 if i % 2 == 0 else float("nan"),
            "neighborhood": "A" if i < 4 else "B",
        })
    return pd.DataFrame(rows), tmp_path
