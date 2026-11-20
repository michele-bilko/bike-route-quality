"""Aerial imagery from MassGIS"""

from __future__ import annotations


def crop_aerial_tiles(segments, out_dir: str, year: int = 2025):
    """Cut one aerial crop around each street segment

    TODO: read 15 centimeter MassGIS orthophotos (spring, leaf-off) for the
    given year, either from downloaded tiles or the web tile service, and save a
    fixed size crop centered on each segment into out_dir. 
    Record the path in the segment table's aerial_path column.

    Source: https://www.mass.gov/info-details/massgis-data-2025-aerial-imagery
    """
    raise NotImplementedError("Planned: crop with rasterio and save to data/processed/aerial/")
