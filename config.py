# config.py

SEARCH_PREFIX = "hiring"

SEARCH_KEYWORDS = [
    "Azure Data Engineer",
    "Microsoft Fabric",
    "Azure Databricks",
    "Azure Data Factory",
    "Pyspark"
]
    
HEADLESS = True

WAIT_TIME = 3000

OUTPUT_DIR = "output"

# -----------------------------------
# Search Filters
# -----------------------------------

SORT_BY = "date_posted"

# Options:
# past-24h
# past-week
# past-month
DATE_POSTED = "past-24h"

# -----------------------------------
# Scrolling Configuration
# -----------------------------------

SCROLL_STEP_MIN = 600
SCROLL_STEP_MAX = 1000

SCROLL_WAIT_MIN = 1800
SCROLL_WAIT_MAX = 3000

RECHECK_WAIT = 1500

MAX_EMPTY_SCROLLS = 5