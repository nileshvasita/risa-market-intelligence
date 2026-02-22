#!/usr/bin/env python3
"""Add latitude/longitude to cancer_centers using static city coordinates."""

import sqlite3
import os
import random

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_intel.db")

# Static coordinates for known cities
CITY_COORDS = {
    # California
    ("San Francisco", "CA"): (37.7749, -122.4194),
    ("Los Angeles", "CA"): (34.0522, -118.2437),
    ("San Diego", "CA"): (32.7157, -117.1611),
    ("Sacramento", "CA"): (38.5816, -121.4944),
    ("Stanford", "CA"): (37.4275, -122.1697),
    ("Duarte", "CA"): (34.1395, -117.9773),
    ("La Jolla", "CA"): (32.8328, -117.2713),
    ("Orange", "CA"): (33.7879, -117.8531),
    ("Torrance", "CA"): (33.8358, -118.3406),
    ("Loma Linda", "CA"): (34.0483, -117.2612),
    ("Riverside", "CA"): (33.9533, -117.3962),
    ("Fresno", "CA"): (36.7378, -119.7871),
    ("Anaheim", "CA"): (33.8366, -117.9143),
    ("Corona", "CA"): (33.8753, -117.5664),
    ("San Luis Obispo", "CA"): (35.2828, -120.6596),
    ("La Verne", "CA"): (34.1008, -117.7678),
    ("Palo Alto", "CA"): (37.4419, -122.1430),
    ("Pleasant Hill", "CA"): (37.9480, -122.0608),
    ("Santa Rosa", "CA"): (38.4404, -122.7141),
    ("Glendale", "CA"): (34.1425, -118.2551),
    ("Fountain Valley", "CA"): (33.7092, -117.9536),
    ("Pomona", "CA"): (34.0551, -117.7500),
    ("Beverly Hills", "CA"): (34.0736, -118.4004),
    ("Chico", "CA"): (39.7285, -121.8375),
    ("Escondido", "CA"): (33.1192, -117.0864),
    ("Fremont", "CA"): (37.5485, -121.9886),
    ("French Camp", "CA"): (37.8808, -121.2703),
    ("Greenbrae", "CA"): (37.9460, -122.5356),
    ("Long Beach", "CA"): (33.7701, -118.1937),
    ("Mountain View", "CA"): (37.3861, -122.0839),
    ("Newport Beach", "CA"): (33.6189, -117.9298),
    ("Irvine", "CA"): (33.6846, -117.8265),
    ("Oxnard", "CA"): (34.1975, -119.1771),
    ("Pasadena", "CA"): (34.1478, -118.1445),
    ("Rancho Mirage", "CA"): (33.7397, -116.4129),
    ("Salinas", "CA"): (36.6777, -121.6555),
    ("San Jose", "CA"): (37.3382, -121.8863),
    ("Santa Monica", "CA"): (34.0195, -118.4912),
    ("Thousand Oaks", "CA"): (34.1706, -118.8376),
    ("Visalia", "CA"): (36.3302, -119.2921),
    ("Walnut Creek", "CA"): (37.9101, -122.0652),
    ("Concord", "CA"): (37.9780, -122.0311),
    ("Whittier", "CA"): (33.9792, -118.0328),
    ("Downey", "CA"): (33.9401, -118.1332),
    ("Oakland", "CA"): (37.8044, -122.2712),
    ("Mission Viejo", "CA"): (33.5965, -117.6590),
    ("Bakersfield", "CA"): (35.3733, -119.0187),
    ("Eureka", "CA"): (40.8021, -124.1637),
    # Texas
    ("Houston", "TX"): (29.7604, -95.3698),
    ("Dallas", "TX"): (32.7767, -96.7970),
    ("Fort Worth", "TX"): (32.7555, -97.3308),
    ("San Antonio", "TX"): (29.4241, -98.4936),
    ("Austin", "TX"): (30.2672, -97.7431),
    ("El Paso", "TX"): (31.7619, -106.4850),
    ("Tyler", "TX"): (32.3513, -95.3011),
    ("Temple", "TX"): (31.0982, -97.3428),
    ("Lubbock", "TX"): (33.5779, -101.8552),
    ("Amarillo", "TX"): (35.2220, -101.8313),
    ("Abilene", "TX"): (32.4487, -99.7331),
    ("Plano", "TX"): (33.0198, -96.6989),
    ("Irving", "TX"): (32.8140, -96.9489),
    ("Round Rock", "TX"): (30.5083, -97.6789),
    ("Bedford", "TX"): (32.8440, -97.1431),
    ("Sherman", "TX"): (33.6357, -96.6089),
    ("Wichita Falls", "TX"): (33.9137, -98.4934),
    ("Midland", "TX"): (31.9973, -102.0779),
    ("McAllen", "TX"): (26.2034, -98.2300),
    ("Longview", "TX"): (32.5007, -94.7405),
    ("Galveston", "TX"): (29.3013, -94.7977),
    ("Bryan", "TX"): (30.6744, -96.3700),
    ("College Station", "TX"): (30.6280, -96.3344),
    ("Corpus Christi", "TX"): (27.8006, -97.3964),
    ("Harlingen", "TX"): (26.1906, -97.6961),
    ("Killeen", "TX"): (31.1171, -97.7278),
    ("Nacogdoches", "TX"): (31.6035, -94.6555),
    ("Odessa", "TX"): (31.8457, -102.3676),
    ("San Angelo", "TX"): (31.4638, -100.4370),
    ("Victoria", "TX"): (28.8053, -96.9850),
    ("Mansfield", "TX"): (32.5632, -97.1417),
    ("Denton", "TX"): (33.2148, -97.1331),
    # Washington
    ("Seattle", "WA"): (47.6062, -122.3321),
    ("Tacoma", "WA"): (47.2529, -122.4443),
    ("Spokane", "WA"): (47.6588, -117.4260),
    ("Olympia", "WA"): (47.0379, -122.9007),
    ("Bellingham", "WA"): (48.7519, -122.4787),
    ("Vancouver", "WA"): (45.6387, -122.6615),
    ("Wenatchee", "WA"): (47.4235, -120.3103),
    ("Yakima", "WA"): (46.6021, -120.5059),
    ("Kennewick", "WA"): (46.2112, -119.1372),
    ("Everett", "WA"): (47.9790, -122.2021),
    ("Bellevue", "WA"): (47.6101, -122.2015),
    ("Bremerton", "WA"): (47.5673, -122.6326),
    ("Burien", "WA"): (47.4704, -122.3468),
    ("Kirkland", "WA"): (47.6815, -122.2087),
    ("Mt. Vernon", "WA"): (48.4201, -122.3346),
    ("Renton", "WA"): (47.4829, -122.2171),
    ("Richland", "WA"): (46.2856, -119.2845),
    ("Walla Walla", "WA"): (46.0646, -118.3430),
    ("Anacortes", "WA"): (48.5126, -122.6127),
    ("Coupeville", "WA"): (48.2198, -122.6858),
    ("Sequim", "WA"): (48.0795, -123.1015),
    ("Port Angeles", "WA"): (48.1187, -123.4307),
    ("Federal Way", "WA"): (47.3223, -122.3126),
    ("Puyallup", "WA"): (47.1854, -122.2929),
    ("Auburn", "WA"): (47.3073, -122.2285),
    ("Coeur d'Alene", "ID"): (47.6777, -116.7805),
}

# State centroids as fallback
STATE_CENTROIDS = {
    "CA": (36.7783, -119.4179),
    "TX": (31.9686, -99.9018),
    "WA": (47.7511, -120.7401),
}


def find_coords(city_str, state):
    """Try to find coordinates for a city string, handling compound cities."""
    if not city_str or city_str == "-":
        return STATE_CENTROIDS.get(state, (37.5, -96.0))

    # Direct match
    key = (city_str, state)
    if key in CITY_COORDS:
        return CITY_COORDS[key]

    # Try first city in compound names like "Dallas/Plano/Denton"
    parts = city_str.replace(",", "/").split("/")
    for part in parts:
        clean = part.strip()
        # Remove parenthetical info
        if "(" in clean:
            clean = clean.split("(")[0].strip()
        if not clean:
            continue
        key = (clean, state)
        if key in CITY_COORDS:
            return CITY_COORDS[key]

    # Try substring match in city names
    for (c, s), coords in CITY_COORDS.items():
        if s == state and c.lower() in city_str.lower():
            return coords

    # Check for "Multiple" or "Statewide" - use state centroid
    lower = city_str.lower()
    if "multiple" in lower or "statewide" in lower:
        return STATE_CENTROIDS.get(state, (37.5, -96.0))

    # Fallback to state centroid
    return STATE_CENTROIDS.get(state, (37.5, -96.0))


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Add columns if they don't exist
    existing = [row[1] for row in c.execute("PRAGMA table_info(cancer_centers)").fetchall()]
    if "latitude" not in existing:
        c.execute("ALTER TABLE cancer_centers ADD COLUMN latitude REAL")
    if "longitude" not in existing:
        c.execute("ALTER TABLE cancer_centers ADD COLUMN longitude REAL")
    conn.commit()

    # Get all centers
    c.execute("SELECT id, city, state FROM cancer_centers")
    rows = c.fetchall()

    # Track city usage for offset
    city_count = {}
    for row in rows:
        city_key = (row["city"], row["state"])
        city_count[city_key] = city_count.get(city_key, 0) + 1

    city_index = {}
    random.seed(42)  # Reproducible offsets

    for row in rows:
        city_key = (row["city"], row["state"])
        lat, lng = find_coords(row["city"], row["state"])

        # Offset duplicates
        idx = city_index.get(city_key, 0)
        total = city_count[city_key]
        if total > 1:
            # Spread in a small circle
            import math
            angle = (2 * math.pi * idx) / total
            offset = 0.02 + 0.01 * (total // 5)
            lat += offset * math.sin(angle)
            lng += offset * math.cos(angle)
        city_index[city_key] = idx + 1

        c.execute(
            "UPDATE cancer_centers SET latitude = ?, longitude = ? WHERE id = ?",
            [round(lat, 6), round(lng, 6), row["id"]]
        )

    conn.commit()
    print("Geocoded {} centers".format(len(rows)))

    # Verify
    c.execute("SELECT COUNT(*) FROM cancer_centers WHERE latitude IS NOT NULL")
    count = c.fetchone()[0]
    print("{} centers have coordinates".format(count))

    conn.close()


if __name__ == "__main__":
    main()
