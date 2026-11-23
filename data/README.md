# Data folder

CLARIFICATION FOR ASSISTANTS ON PROJECT: Nothing in this folder gets committed to git except this file (see `.gitignore`).
The downloads of data (especially the quantity and quality of images we are using) can be large, and some sources need attribution, so each person will need to rebuild the data locally with the collection code in `src/bikeroute/sources/`.

Planned layout (NOT YET IMPLEMENTED):
```
data/
  raw/
    osm/          street network and tags from OpenStreetMap
    aerial/       MassGIS 15 centimeter aerial imagery tiles
    street_level/ Mapillary photos (attribution required, CC BY-SA 4.0)
    labels/       stress ratings, bike facility types, crash records
  processed/
    segments.csv  one row per street segment with columns defined in src/bikeroute/schema.py
    aerial/       one crop per segment
    street/       street level photos matched to segments
```

## Sources

| Street segments and tags | OpenStreetMap | Open Database Licence |
| Aerial imagery | MassGIS 2025 Aerial Imagery | Public Massachusetts data |
| Street level photos | Mapillary | CC BY-SA 4.0, attribution required |
| Stress ratings | Boston Cyclists Union Labs Bike Stress Map; City of Boston Bicycle Level of Traffic Stress map | WAITING TO BE CONFIRMED |
| Bike facility types | MassDOT Bike Inventory 2020; City of Boston Existing Bike Network | Public |
| Crash history | Boston Vision Zero crash records | Public |

REMINDER: NEVER COMMIT ACCESS TOKENS. 
Mapillary's token is read from the environment variable
`MAPILLARY_ACCESS_TOKEN`.
