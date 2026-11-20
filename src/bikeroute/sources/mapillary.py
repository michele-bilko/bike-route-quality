"""Street level photos from Mapillary"""

from __future__ import annotations

import os


def fetch_street_images(segments, out_dir: str):
    """Download the nearest street level photo for each segment

    TODO: query Mapillary's API for photos near each segment,
    prefer recent ones, record each photo's capture date and author (for the
    CC BY-SA attribution requirement), and save the files into out_dir

    The access token comes from the MAPILLARY_ACCESS_TOKEN environment variable.
    NEVER COMMIT OR ENTER THIS IN PLAINTEXT IN THE CODEBASE

    Docs: https://www.mapillary.com/developer
    """
    token = os.environ.get("MAPILLARY_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Set the MAPILLARY_ACCESS_TOKEN environment variable first")
    raise NotImplementedError("Planned: query the Mapillary API and save to data/processed/street/")
