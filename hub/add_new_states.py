#!/usr/bin/env python3
"""
Parse cancer-centers-FL-NY-MA.md and insert new centers into the existing
market_intel.db SQLite database. Idempotent - skips centers that already exist.
Adds latitude/longitude via a city coordinate dictionary.

Python 3.9 compatible.
"""

import os
import re
import sqlite3
import sys
from typing import List, Tuple, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")
MD_PATH = os.path.join(PARENT_DIR, "data", "cancer-centers-FL-NY-MA.md")

# ---------------------------------------------------------------------------
# City coordinate dictionary (lat, lng) for geocoding
# ---------------------------------------------------------------------------
CITY_COORDS = {
    # Florida
    "Tampa": (27.9506, -82.4572),
    "Miami": (25.7617, -80.1918),
    "Jacksonville": (30.3322, -81.6557),
    "Gainesville": (29.6516, -82.3248),
    "Orlando": (28.5383, -81.3792),
    "Boca Raton": (26.3683, -80.1289),
    "Tallahassee": (30.4383, -84.2807),
    "Fort Myers": (26.6406, -81.8723),
    "Port St. Lucie": (27.2730, -80.3582),
    "Stuart": (27.1976, -80.2528),
    "Ocoee": (28.5692, -81.5440),
    "Titusville": (28.6122, -80.8076),
    "Melbourne": (28.0836, -80.6081),
    "Plantation": (26.1276, -80.2331),
    "New Port Richey": (28.2442, -82.7193),
    "Hollywood": (26.0112, -80.1495),
    "Pembroke Pines": (26.0128, -80.3382),
    "Weston": (26.1004, -80.3998),
    "Cape Coral": (26.5629, -81.9495),
    "Sarasota": (27.3364, -82.5307),
    "Naples": (26.1420, -81.7948),
    "Fort Lauderdale": (26.1224, -80.1373),
    "Miami Beach": (25.7907, -80.1300),
    "Jupiter": (26.9342, -80.0942),
    "Daytona Beach": (29.2108, -81.0228),
    "Lakeland": (28.0395, -81.9498),
    "St. Petersburg": (27.7676, -82.6403),
    "Wesley Chapel": (28.2397, -82.3276),
    # New York
    "New York": (40.7128, -74.0060),
    "Buffalo": (42.8864, -78.8784),
    "Stony Brook": (40.9257, -73.1409),
    "Rochester": (43.1566, -77.6088),
    "Syracuse": (43.0481, -76.1474),
    "Albany": (42.6526, -73.7562),
    "Brooklyn": (40.6782, -73.9442),
    "Valhalla": (41.0748, -73.7707),
    "Bronx": (40.8448, -73.8648),
    "Cold Spring Harbor": (40.8715, -73.4568),
    "Mineola": (40.7493, -73.6407),
    "New Hyde Park": (40.7351, -73.6879),
    "Cooperstown": (42.6995, -74.9246),
    "Middletown": (41.4459, -74.4229),
    "Uniondale": (40.7001, -73.5935),
    "Harrison": (41.0301, -73.7126),
    "East Setauket": (40.9462, -73.1101),
    "Poughkeepsie": (41.7004, -73.9210),
    "Newburgh": (41.5034, -74.0104),
    "Sayre": (41.9789, -76.5155),
    "Corning": (42.1428, -77.0547),
    # Massachusetts
    "Boston": (42.3601, -71.0589),
    "Worcester": (42.2626, -71.8023),
    "Springfield": (42.1015, -72.5898),
    "Burlington": (42.5048, -71.1956),
    "Hyannis": (41.6529, -70.2828),
    "Pittsfield": (42.4501, -73.2454),
    "Weymouth": (42.2188, -70.9395),
    "Brighton": (42.3484, -71.1527),
    "Brockton": (42.0834, -71.0184),
    "Concord": (42.4604, -71.3489),
    "Newton": (42.3370, -71.2092),
    "Framingham": (42.2793, -71.4162),
    "Attleboro": (41.9445, -71.2856),
    "Lowell": (42.6334, -71.3162),
    "Northampton": (42.3251, -72.6412),
    "Milford": (42.1398, -71.5164),
    "Gardner": (42.5751, -71.9981),
    "Southbridge": (42.0751, -72.0334),
    "Winchester": (42.4523, -71.1370),
    "Cambridge": (42.3736, -71.1097),
    "Brewster": (41.7601, -70.0820),
    "New Bedford": (41.6362, -70.9342),
    "Fall River": (41.7015, -71.1550),
    "Fairhaven": (41.6378, -70.9037),
    "Peabody": (42.5279, -70.9287),
    "Greenfield": (42.5876, -72.5995),
    "Danvers": (42.5751, -70.9301),
    "Plymouth": (41.9584, -70.6673),
    "Waltham": (42.3765, -71.2356),
}

# Map state header text to abbreviation
STATE_MAP = {
    "FLORIDA": "FL",
    "NEW YORK": "NY",
    "MASSACHUSETTS": "MA",
}


def parse_md(path: str) -> List[Tuple[str, str, str, str, str, str, str, str]]:
    """Parse the markdown file and return list of center tuples.

    Returns tuples of:
        (name, city, state, category, parent_org, est_oncologists, website, nci_type)
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    rows = []
    lines = content.split("\n")
    current_state = ""
    current_category = ""

    for line in lines:
        # Detect state headers
        sm = re.match(r"^#\s+(FLORIDA|NEW YORK|MASSACHUSETTS)\s*$", line.strip(), re.IGNORECASE)
        if sm:
            current_state = STATE_MAP.get(sm.group(1).upper(), "")
            continue

        # Detect category headers
        cm = re.match(r"^##\s+\d+\.\s+(.+?)(?:\s*\(\d+\))?\s*$", line.strip())
        if cm:
            current_category = cm.group(1).strip()
            continue

        # Parse table rows
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]

        if len(cells) < 3:
            continue
        if cells[0] == "#" or re.match(r"^[-:]+$", cells[0]):
            continue
        if not re.match(r"^\d+$", cells[0]):
            continue

        name = re.sub(r"\*\*", "", cells[1]).strip()
        city = re.sub(r"\*\*", "", cells[2]).strip()

        nci_type = ""
        parent_org = ""
        est_onc = ""
        website = ""

        if "NCI" in current_category.upper():
            nci_type = cells[3] if len(cells) > 3 else ""
            parent_org = cells[4] if len(cells) > 4 else ""
            est_onc = cells[5] if len(cells) > 5 else ""
            website = cells[6] if len(cells) > 6 else ""
        elif "Academic" in current_category:
            parent_org = cells[3] if len(cells) > 3 else ""
            est_onc = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Community" in current_category:
            est_onc = cells[3] if len(cells) > 3 else ""
            parent_org = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Hospital" in current_category:
            parent_org = cells[3] if len(cells) > 3 else ""
            est_onc = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Specialty" in current_category or "Boutique" in current_category:
            nci_type = cells[3] if len(cells) > 3 else ""
            parent_org = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""

        # Clean markdown formatting
        for val in [est_onc, parent_org, website, nci_type]:
            val = re.sub(r"\*\*", "", val).strip()

        est_onc = re.sub(r"\*\*", "", est_onc).strip()
        parent_org = re.sub(r"\*\*", "", parent_org).strip()
        website = re.sub(r"\*\*", "", website).strip()
        nci_type = re.sub(r"\*\*", "", nci_type).strip()

        rows.append((name, city, current_state, current_category, parent_org, est_onc, website, nci_type))

    return rows


def geocode(city: str) -> Tuple[Optional[float], Optional[float]]:
    """Look up lat/lng for a city from the coordinate dictionary.

    Tries exact match first, then partial match on first token.
    """
    if not city:
        return (None, None)

    # Try exact match
    if city in CITY_COORDS:
        return CITY_COORDS[city]

    # Try first city if "City/City" format
    first = city.split("/")[0].strip()
    if first in CITY_COORDS:
        return CITY_COORDS[first]

    # Try matching after removing "Multiple" prefix or parentheticals
    clean = re.sub(r"\(.*?\)", "", city).strip()
    clean = re.sub(r"^Multiple\s*", "", clean).strip()
    first_clean = clean.split("/")[0].split(",")[0].strip()
    if first_clean in CITY_COORDS:
        return CITY_COORDS[first_clean]

    return (None, None)


def ensure_columns(conn: sqlite3.Connection) -> None:
    """Add latitude/longitude columns if they don't exist."""
    c = conn.cursor()
    c.execute("PRAGMA table_info(cancer_centers)")
    cols = {row[1] for row in c.fetchall()}
    if "latitude" not in cols:
        c.execute("ALTER TABLE cancer_centers ADD COLUMN latitude REAL")
    if "longitude" not in cols:
        c.execute("ALTER TABLE cancer_centers ADD COLUMN longitude REAL")
    conn.commit()


def get_existing_names(conn: sqlite3.Connection) -> set:
    """Return set of existing center names (lowercased for comparison)."""
    c = conn.cursor()
    c.execute("SELECT name FROM cancer_centers")
    return {row[0].lower().strip() for row in c.fetchall() if row[0]}


def main() -> None:
    if not os.path.exists(MD_PATH):
        print("ERROR: Markdown file not found: {}".format(MD_PATH))
        sys.exit(1)

    if not os.path.exists(DB_PATH):
        print("ERROR: Database not found: {}".format(DB_PATH))
        print("Run build_db.py first to create the database.")
        sys.exit(1)

    print("Parsing {}...".format(os.path.basename(MD_PATH)))
    rows = parse_md(MD_PATH)
    print("  Found {} centers in markdown".format(len(rows)))

    conn = sqlite3.connect(DB_PATH)
    ensure_columns(conn)
    existing = get_existing_names(conn)

    inserted = 0
    skipped = 0
    geocoded = 0
    c = conn.cursor()

    for name, city, state, category, parent_org, est_onc, website, nci_type in rows:
        if name.lower().strip() in existing:
            skipped += 1
            continue

        lat, lng = geocode(city)
        if lat is not None:
            geocoded += 1

        c.execute(
            """INSERT INTO cancer_centers
               (name, city, state, category, parent_org, est_oncologists, website, nci_type, latitude, longitude)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, city, state, category, parent_org, est_onc, website, nci_type, lat, lng),
        )
        inserted += 1
        existing.add(name.lower().strip())

    conn.commit()
    conn.close()

    print("\nResults:")
    print("  Inserted: {}".format(inserted))
    print("  Skipped (already exist): {}".format(skipped))
    print("  Geocoded: {} of {} inserted".format(geocoded, inserted))
    print("\nDatabase updated: {}".format(DB_PATH))


if __name__ == "__main__":
    main()
