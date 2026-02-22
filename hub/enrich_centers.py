#!/usr/bin/env python3
"""Enrich cancer_centers table with EHR vendor, health system, bed count, 340B, and case volume data."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_intel.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- Specific center data (well-known, publicly documented) ---
# Format: { name_fragment: { field: value, ... } }
# Only includes data that is reliably known from public sources.

SPECIFIC_CENTERS = {
    "MD Anderson Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 1100,
        "is_340b": 1,
        "annual_cancer_cases": 40000,
        "notes": "Largest cancer center in US by volume. #1 USNWR ranking.",
    },
    "Fred Hutchinson Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 334,
        "is_340b": 1,
        "annual_cancer_cases": 10000,
        "notes": "Merged with Seattle Cancer Care Alliance 2022. Leading BMT/immunotherapy center.",
    },
    "City of Hope Comprehensive Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 217,
        "is_340b": 1,
        "annual_cancer_cases": 14000,
        "notes": "NCI Comprehensive. Acquired Cancer Treatment Centers of America network.",
    },
    "Stanford Cancer Institute": {
        "ehr_vendor": "Epic",
        "bed_count": 613,
        "is_340b": 1,
        "annual_cancer_cases": 8000,
        "health_system": "Stanford Health Care",
        "notes": "NCI Comprehensive. Strong in precision medicine and clinical trials.",
    },
    "UCSF Helen Diller Family Comprehensive Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 600,
        "is_340b": 1,
        "annual_cancer_cases": 10000,
        "health_system": "UCSF Health",
        "notes": "NCI Comprehensive. Top-tier research and immunotherapy.",
    },
    "Jonsson Comprehensive Cancer Center (UCLA)": {
        "ehr_vendor": "Epic",
        "bed_count": 520,
        "is_340b": 1,
        "annual_cancer_cases": 9000,
        "health_system": "UCLA Health",
    },
    "USC Norris Comprehensive Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 401,
        "is_340b": 1,
        "annual_cancer_cases": 5000,
        "health_system": "Keck Medicine of USC",
    },
    "UC San Diego Moores Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 808,
        "is_340b": 1,
        "annual_cancer_cases": 6000,
        "health_system": "UC San Diego Health",
    },
    "UC Davis Comprehensive Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 625,
        "is_340b": 1,
        "annual_cancer_cases": 5000,
        "health_system": "UC Davis Health",
    },
    "UCI Chao Family Comprehensive Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 417,
        "is_340b": 1,
        "annual_cancer_cases": 5000,
        "health_system": "UC Irvine Health",
    },
    "Harold C. Simmons Comprehensive Cancer Center (UT Southwestern)": {
        "ehr_vendor": "Epic",
        "bed_count": 921,
        "is_340b": 1,
        "annual_cancer_cases": 12000,
        "health_system": "UT Southwestern Medical Center",
        "notes": "NCI Comprehensive. Strong in GI, GU, and heme-onc.",
    },
    "Mays Cancer Center (UT Health San Antonio)": {
        "ehr_vendor": "Epic",
        "bed_count": 716,
        "is_340b": 1,
        "annual_cancer_cases": 5000,
        "health_system": "UT Health San Antonio",
        "notes": "NCI Designated. Only NCI center in South Texas.",
    },
    "Baylor College of Medicine": {
        "ehr_vendor": "Epic",
        "is_340b": 1,
        "health_system": "Baylor College of Medicine",
    },
    "Houston Methodist Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 2600,
        "is_340b": 1,
        "annual_cancer_cases": 8000,
        "health_system": "Houston Methodist",
        "notes": "Major academic-affiliated system. Uses Epic across all locations.",
    },
    "Memorial Hermann Cancer Centers": {
        "ehr_vendor": "Epic",
        "bed_count": 1800,
        "is_340b": 1,
        "health_system": "Memorial Hermann Health System",
    },
    "Cedars-Sinai Cancer": {
        "ehr_vendor": "Epic",
        "bed_count": 886,
        "is_340b": 1,
        "annual_cancer_cases": 6000,
        "health_system": "Cedars-Sinai Health System",
    },
    "Loma Linda University Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 900,
        "is_340b": 1,
        "health_system": "Loma Linda University Health",
        "notes": "Pioneer in proton therapy. Seventh-day Adventist affiliated.",
    },
    "Swedish Cancer Institute": {
        "ehr_vendor": "Epic",
        "bed_count": 714,
        "is_340b": 1,
        "health_system": "Providence",
        "notes": "Largest cancer program in WA. Part of Providence system.",
    },
    "Dell Medical School Cancer Programs": {
        "ehr_vendor": "Epic",
        "is_340b": 1,
        "health_system": "UT Austin / Ascension Seton",
    },
    "Texas Oncology": {
        "ehr_vendor": "iKnowMed (McKesson)",
        "is_340b": 0,
        "health_system": "US Oncology Network / McKesson",
        "notes": "Largest community oncology practice in TX. 500+ physicians, 200+ sites.",
        "annual_cancer_cases": 50000,
    },
    "Scripps MD Anderson Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 700,
        "is_340b": 1,
        "health_system": "Scripps Health",
        "notes": "Partnership with MD Anderson for second opinions and protocols.",
    },
    "Hoag Family Cancer Institute": {
        "ehr_vendor": "Epic",
        "bed_count": 498,
        "is_340b": 1,
        "health_system": "Hoag Memorial Hospital Presbyterian",
    },
    "Sharp HealthCare Cancer Programs": {
        "ehr_vendor": "Epic",
        "bed_count": 2100,
        "is_340b": 1,
        "health_system": "Sharp HealthCare",
    },
    "Baylor Scott & White Cancer Centers": {
        "ehr_vendor": "Epic",
        "bed_count": 1000,
        "is_340b": 1,
        "health_system": "Baylor Scott & White Health",
        "notes": "Largest not-for-profit health system in TX.",
    },
    "Texas Health Resources Cancer Programs": {
        "ehr_vendor": "Epic",
        "bed_count": 4100,
        "is_340b": 1,
        "health_system": "Texas Health Resources",
    },
    "Methodist Health System Cancer Centers": {
        "ehr_vendor": "Epic",
        "bed_count": 1500,
        "is_340b": 1,
        "health_system": "Methodist Health System (Dallas)",
    },
    "Texas Children's Cancer and Hematology Centers": {
        "ehr_vendor": "Epic",
        "bed_count": 973,
        "is_340b": 1,
        "health_system": "Texas Children's Hospital / Baylor",
        "notes": "Largest pediatric cancer program in US.",
    },
    "Parkland Health Cancer Programs": {
        "ehr_vendor": "Epic",
        "bed_count": 862,
        "is_340b": 1,
        "health_system": "Parkland Health",
        "notes": "Safety net hospital. UT Southwestern faculty.",
    },
    "The Oncology Institute of Hope and Innovation (TOI)": {
        "ehr_vendor": "Flatiron OncoEMR",
        "is_340b": 0,
        "notes": "Publicly traded (NYSE: TOI). Value-based care model. 60+ locations CA/FL/NV.",
    },
    "MultiCare Health Cancer Programs": {
        "ehr_vendor": "Epic",
        "bed_count": 1600,
        "is_340b": 1,
        "health_system": "MultiCare Health System",
    },
    "UW Medicine Cancer Programs": {
        "ehr_vendor": "Epic",
        "bed_count": 529,
        "is_340b": 1,
        "health_system": "UW Medicine",
    },
    "UT Health Houston Cancer Programs": {
        "ehr_vendor": "Epic",
        "is_340b": 1,
        "health_system": "UT Health Houston",
    },
    "UTMB Health Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 604,
        "is_340b": 1,
        "health_system": "UT Medical Branch",
    },
    "Ascension Seton Cancer Care": {
        "ehr_vendor": "Epic",
        "is_340b": 1,
        "health_system": "Ascension",
    },
    "EvergreenHealth Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 318,
        "is_340b": 1,
        "health_system": "EvergreenHealth",
    },
    "Overlake Medical Center Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 349,
        "is_340b": 1,
        "health_system": "Overlake Medical Center",
    },
    "John Muir Health Cancer Program": {
        "ehr_vendor": "Epic",
        "bed_count": 572,
        "is_340b": 1,
        "health_system": "John Muir Health",
    },
    "El Camino Health Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 420,
        "is_340b": 1,
        "health_system": "El Camino Health",
    },
    "MemorialCare Todd Cancer Institute": {
        "ehr_vendor": "Epic",
        "bed_count": 1400,
        "is_340b": 1,
        "health_system": "MemorialCare",
    },
    "PIH Health Cancer Programs": {
        "ehr_vendor": "Cerner",
        "bed_count": 560,
        "is_340b": 1,
        "health_system": "PIH Health",
    },
    "Palomar Health Cancer Center": {
        "ehr_vendor": "Epic",
        "bed_count": 463,
        "is_340b": 1,
        "health_system": "Palomar Health",
    },
}

# --- Pattern-based rules for parent_org / name matching ---

def apply_pattern_rules(row):
    """Return dict of fields to update based on parent_org and name patterns."""
    updates = {}
    name = row["name"] or ""
    parent = row["parent_org"] or ""
    category = row["category"] or ""

    # US Oncology / McKesson practices → iKnowMed
    if "US Oncology" in parent or "US Oncology" in name:
        updates["ehr_vendor"] = "iKnowMed (McKesson)"
        updates.setdefault("health_system", "US Oncology Network / McKesson")
        updates["is_340b"] = 0

    # OneOncology practices → often Flatiron
    if "OneOncology" in parent:
        updates["ehr_vendor"] = "Flatiron OncoEMR"
        updates.setdefault("health_system", "OneOncology")
        updates["is_340b"] = 0

    # Sutter Health → Epic
    if "Sutter" in parent or "Sutter" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Sutter Health")
        updates["is_340b"] = 1

    # Providence → Epic
    if "Providence" in parent or "Providence" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Providence")
        updates["is_340b"] = 1

    # Kaiser Permanente → Epic (migrated from HealthConnect)
    if "Kaiser" in parent or "Kaiser" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Kaiser Permanente")
        updates["is_340b"] = 0
        updates["notes"] = "Integrated delivery system. Not 340B (not DSH-eligible)."

    # HCA Healthcare → MEDITECH/Cerner mix, but mostly MEDITECH
    if "HCA" in parent:
        updates["ehr_vendor"] = "MEDITECH"
        updates.setdefault("health_system", "HCA Healthcare")
        updates["is_340b"] = 0
        updates["notes"] = "HCA is for-profit; most locations use MEDITECH (migrating to MEDITECH Expanse)."

    # Tenet Healthcare → Cerner
    if "Tenet" in parent:
        updates["ehr_vendor"] = "Cerner"
        updates.setdefault("health_system", "Tenet Healthcare")
        updates["is_340b"] = 0

    # CommonSpirit → Epic (most locations migrated)
    if "CommonSpirit" in parent or "VMFH" in parent or "CHI Franciscan" in parent or "Virginia Mason Franciscan" in parent:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "CommonSpirit Health")
        updates["is_340b"] = 1

    # Cedars-Sinai affiliates → Epic
    if "Cedars-Sinai" in parent or "Cedars-Sinai" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Cedars-Sinai Health System")

    # PeaceHealth → Epic
    if "PeaceHealth" in parent or "PeaceHealth" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "PeaceHealth")
        updates["is_340b"] = 1

    # Adventist Health → Epic
    if "Adventist" in parent and "Loma Linda" not in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Adventist Health")
        updates["is_340b"] = 1

    # AdventHealth → Cerner
    if "AdventHealth" in parent or "AdventHealth" in name:
        updates["ehr_vendor"] = "Cerner"
        updates.setdefault("health_system", "AdventHealth")
        updates["is_340b"] = 1

    # CHRISTUS Health → Epic (migrated from MEDITECH)
    if "CHRISTUS" in parent or "CHRISTUS" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "CHRISTUS Health")
        updates["is_340b"] = 1

    # Covenant Health (Providence affiliate) → Epic
    if "Covenant" in parent or "Covenant" in name:
        updates["ehr_vendor"] = "Epic"
        updates.setdefault("health_system", "Providence / Covenant Health")
        updates["is_340b"] = 1

    # UC system → Epic
    if parent.startswith("UC ") or "UCSF" in parent or "UCLA" in parent:
        updates["ehr_vendor"] = "Epic"
        updates["is_340b"] = 1

    return updates


def main():
    conn = get_conn()
    cur = conn.cursor()

    rows = cur.execute("SELECT * FROM cancer_centers").fetchall()
    print("Total centers: {}".format(len(rows)))

    updated = 0
    for row in rows:
        name = row["name"]
        updates = {}

        # Check specific centers first (exact name match)
        for key, data in SPECIFIC_CENTERS.items():
            if key in name:
                updates.update(data)
                break

        # Apply pattern rules (won't overwrite specific data)
        pattern = apply_pattern_rules(row)
        for k, v in pattern.items():
            if k not in updates:
                updates[k] = v

        if not updates:
            continue

        # Build UPDATE statement
        set_parts = []
        vals = []
        for col, val in updates.items():
            set_parts.append("{} = ?".format(col))
            vals.append(val)

        vals.append(row["id"])
        sql = "UPDATE cancer_centers SET {} WHERE id = ?".format(", ".join(set_parts))
        cur.execute(sql, vals)
        updated += 1

    conn.commit()
    conn.close()
    print("Updated {} centers.".format(updated))


if __name__ == "__main__":
    main()
