"""Column names of the segment table: one row per street segment

Every module reads and writes the table through these constants, so a column is
renamed in exactly one place. The table is saved as a comma separated file.
"""

# Required columns
SEGMENT_ID = "segment_id"      # stable identifier, e.g. from OpenStreetMap
AERIAL_PATH = "aerial_path"    # aerial crop around the segment, relative to image_root
STRESS_LEVEL = "stress_level"  # Level of Traffic Stress, 1 (comfortable) to 4 (stressful)

# Optional columns
STREET_PATH = "street_path"      # nearest street level photo; blank when none exists
QUALITY_SCORE = "quality_score"  # continuous score 0 to 1; may be blank for many rows
NEIGHBORHOOD = "neighborhood"    # used to hold out entire neighborhoods for testing
FACILITY_TYPE = "facility_type"  # bike facility type from the state or city inventory
CRASH_COUNT = "crash_count"      # bicycle crashes near the segment
IMAGERY_DATE = "imagery_date"    # date of the street level photo

NUM_STRESS_LEVELS = 4
