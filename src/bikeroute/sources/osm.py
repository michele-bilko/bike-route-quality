"""Street network and tags from OpenStreetMap"""

from __future__ import annotations


def fetch_street_segments(place: str):
    """Return a table of street segments for a place, one row per segment

    TODO: use the osmnx package to download the drivable and bikeable street
    network, keep tags that describe cycling conditions (cycleway, maxspeed,
    parking, lanes), and give every segment a stable identifier.

    Example place: "Boston, Massachusetts, USA".
    """
    raise NotImplementedError("Planned: download with osmnx and save to data/raw/osm/")
