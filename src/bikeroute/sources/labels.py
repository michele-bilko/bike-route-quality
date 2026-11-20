"""Labels and safety context for each street segment"""

from __future__ import annotations


def attach_labels(segments):
    """Add stress ratings, facility types and crash counts to the segment table

    TODO: Planned sources, in order of priority:
      1. Boston Cyclists Union Labs Bike Stress Map ratings (request pending)
      2. City of Boston Bicycle Level of Traffic Stress map, as second rating
      3. MassDOT Bike Inventory and City of Boston Existing Bike Network, for
         facility type (shared use path, bike lane, separated bike lane, etc)
      4. Boston Vision Zero crash records, matched to nearby segments

    Both stress ratings are computed from street attributes, not from images, so
    segments where they disagree need to be hand audited
    """
    raise NotImplementedError("Planned: join each source to segments by location")
