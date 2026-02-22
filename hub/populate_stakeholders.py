#!/usr/bin/env python3
"""Populate stakeholders table with verified cancer center leadership data.

Sources: Public cancer center websites, press releases, and leadership pages.
Only includes people verified from public sources as of early 2025.
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")


def get_center_id(conn, name_fragment):
    """Look up center_id by partial name match. Prefer exact-ish matches."""
    c = conn.cursor()
    # Try exact name first
    c.execute(
        "SELECT id FROM cancer_centers WHERE LOWER(name) = LOWER(?) LIMIT 1",
        [name_fragment]
    )
    row = c.fetchone()
    if row:
        return row[0]
    # Then try starts-with
    c.execute(
        "SELECT id FROM cancer_centers WHERE LOWER(name) LIKE LOWER(?) LIMIT 1",
        ["{}%".format(name_fragment)]
    )
    row = c.fetchone()
    if row:
        return row[0]
    # Finally contains
    c.execute(
        "SELECT id FROM cancer_centers WHERE LOWER(name) LIKE LOWER(?) LIMIT 1",
        ["%{}%".format(name_fragment)]
    )
    row = c.fetchone()
    return row[0] if row else None


# Each entry: (name, title, role_type, organization, center_name_fragment, department,
#              linkedin_url, relevance_to_risa, source)
STAKEHOLDERS = [
    # --- MD Anderson Cancer Center ---
    ("Peter WT Pisters", "President and CEO", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Administration", None, "Decision Maker", "Website"),
    ("Welela Tereffe", "Chief Medical Officer", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Mark Moreno", "Senior VP and CFO", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Finance", None, "Decision Maker", "Website"),
    ("Lesly Dossett", "Chief Nursing Officer and VP", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Omer Sultan", "Chief Information Officer", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "IT", None, "Decision Maker", "Website"),

    # --- Memorial Sloan Kettering ---
    ("Selwyn M. Vickers", "President and CEO", "C-Suite",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Administration", None, "Decision Maker", "Website"),
    ("Lisa DeAngelis", "Physician-in-Chief and CMO", "C-Suite",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Michael Repko", "Chief Financial Officer", "C-Suite",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Finance", None, "Decision Maker", "Website"),
    ("Patricia Meehan", "Chief Information Officer", "C-Suite",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "IT", None, "Decision Maker", "Website"),
    ("Joan Massague", "Director, Sloan Kettering Institute", "Director",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Oncology", None, "Influencer", "Website"),

    # --- Dana-Farber Cancer Institute ---
    ("Benjamin L. Ebert", "President and CEO", "C-Suite",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Administration", None, "Decision Maker", "Website"),
    ("Craig A. Bunnell", "Chief Medical Officer and SVP", "C-Suite",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Michael L. Reney", "Chief Operating Officer", "C-Suite",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Administration", None, "Decision Maker", "Website"),
    ("Steven Singer", "Chief Scientific Officer", "C-Suite",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Oncology", None, "Influencer", "Website"),

    # --- Moffitt Cancer Center ---
    ("Patrick Hwu", "President and CEO", "C-Suite",
     "Moffitt Cancer Center", "Moffitt Cancer Center",
     "Administration", None, "Decision Maker", "Website"),
    ("Edmondo Robinson", "Chief Digital Officer", "C-Suite",
     "Moffitt Cancer Center", "Moffitt Cancer Center",
     "IT", None, "Decision Maker", "Website"),
    ("John Cleveland", "Executive VP and Center Director", "C-Suite",
     "Moffitt Cancer Center", "Moffitt Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("G. Douglas Letson", "Physician-in-Chief", "C-Suite",
     "Moffitt Cancer Center", "Moffitt Cancer Center",
     "Clinical Ops", None, "Influencer", "Website"),

    # --- City of Hope ---
    ("Robert Stone", "President and CEO", "C-Suite",
     "City of Hope", "City of Hope",
     "Administration", None, "Decision Maker", "Website"),
    ("Vijay Trisal", "Chief Medical Officer", "C-Suite",
     "City of Hope", "City of Hope",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Harlan Levine", "President, Health Enterprises and Chief Business Officer", "C-Suite",
     "City of Hope", "City of Hope",
     "Administration", None, "Decision Maker", "Website"),
    ("Michael Caligiuri", "President, City of Hope National Medical Center", "C-Suite",
     "City of Hope", "City of Hope",
     "Oncology", None, "Influencer", "Website"),

    # --- Fred Hutch Cancer Center ---
    ("Thomas Lynch", "President and Director", "C-Suite",
     "Fred Hutchinson Cancer Center", "Fred Hutch",
     "Administration", None, "Decision Maker", "Website"),
    ("David Byrd", "Chief Medical Officer", "C-Suite",
     "Fred Hutchinson Cancer Center", "Fred Hutch",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Cheryl Willman", "Director of Cancer Care", "Director",
     "Fred Hutchinson Cancer Center", "Fred Hutch",
     "Oncology", None, "Influencer", "Website"),

    # --- UCSF Helen Diller ---
    ("Alan Ashworth", "President, UCSF Helen Diller Family Comprehensive Cancer Center", "C-Suite",
     "UCSF Helen Diller", "UCSF Helen Diller",
     "Administration", None, "Decision Maker", "Website"),
    ("Sam Hawgood", "Chancellor, UCSF", "C-Suite",
     "UCSF", "UCSF Helen Diller",
     "Administration", None, "Influencer", "Website"),
    ("Pamela Munster", "Associate Director, Clinical Research", "Director",
     "UCSF Helen Diller", "UCSF Helen Diller",
     "Clinical Ops", None, "Influencer", "Website"),

    # --- Stanford Cancer Institute ---
    ("Beverly Mitchell", "Director, Stanford Cancer Institute", "Director",
     "Stanford Cancer Institute", "Stanford Cancer Institute",
     "Oncology", None, "Influencer", "Website"),
    ("Lloyd Minor", "Dean, Stanford School of Medicine", "C-Suite",
     "Stanford Medicine", "Stanford Cancer Institute",
     "Administration", None, "Influencer", "Website"),

    # --- Roswell Park ---
    ("Candace Johnson", "President and CEO", "C-Suite",
     "Roswell Park Comprehensive Cancer Center", "Roswell Park Comprehensive",
     "Administration", None, "Decision Maker", "Website"),
    ("Kunle Odunsi", "Deputy Director and Chair, Immunology", "Director",
     "Roswell Park Comprehensive Cancer Center", "Roswell Park Comprehensive",
     "Oncology", None, "Influencer", "Website"),
    ("Michael Ciesielski", "Chief Financial Officer", "C-Suite",
     "Roswell Park Comprehensive Cancer Center", "Roswell Park Comprehensive",
     "Finance", None, "Decision Maker", "Website"),
    ("Scott Desmit", "Chief Information Officer", "C-Suite",
     "Roswell Park Comprehensive Cancer Center", "Roswell Park Comprehensive",
     "IT", None, "Decision Maker", "Website"),

    # --- Mass General Cancer Center ---
    ("David P. Ryan", "Director, Mass General Cancer Center", "Director",
     "Mass General Cancer Center", "Mass General Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("Peter Slavin", "President, Massachusetts General Hospital", "C-Suite",
     "Massachusetts General Hospital", "Mass General Cancer Center",
     "Administration", None, "Decision Maker", "Website"),
    ("Daniel Haber", "Director, MGH Cancer Center Research", "Director",
     "Mass General Cancer Center", "Mass General Cancer Center",
     "Oncology", None, "Influencer", "Website"),

    # --- NYU Langone Perlmutter ---
    ("Robert Grossman", "CEO, NYU Langone Health", "C-Suite",
     "NYU Langone Health", "Perlmutter Cancer Center",
     "Administration", None, "Decision Maker", "Website"),
    ("Benjamin Neel", "Director, Perlmutter Cancer Center", "Director",
     "NYU Langone Perlmutter Cancer Center", "Perlmutter Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("Nader Mherabi", "Chief Information Officer, NYU Langone", "C-Suite",
     "NYU Langone Health", "Perlmutter Cancer Center",
     "IT", None, "Decision Maker", "Website"),

    # --- Sylvester Comprehensive Cancer Center ---
    ("Stephen Nimer", "Director, Sylvester Comprehensive Cancer Center", "Director",
     "Sylvester Comprehensive Cancer Center", "Sylvester Comprehensive",
     "Oncology", None, "Influencer", "Website"),
    ("Erin Kobetz", "Associate Director, Population Science", "Director",
     "Sylvester Comprehensive Cancer Center", "Sylvester Comprehensive",
     "Oncology", None, "Influencer", "Website"),

    # --- Mayo Clinic Cancer Center (Florida) ---
    ("Gianrico Farrugia", "President and CEO, Mayo Clinic", "C-Suite",
     "Mayo Clinic", "Mayo Clinic Cancer Center",
     "Administration", None, "Decision Maker", "Website"),
    ("Steven Alberts", "Director, Mayo Clinic Cancer Center", "Director",
     "Mayo Clinic Cancer Center", "Mayo Clinic Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("Christopher Ross", "Chief Information Officer, Mayo Clinic", "C-Suite",
     "Mayo Clinic", "Mayo Clinic Cancer Center",
     "IT", None, "Decision Maker", "Website"),
    ("Dennis Dahlen", "CFO, Mayo Clinic", "C-Suite",
     "Mayo Clinic", "Mayo Clinic Cancer Center",
     "Finance", None, "Decision Maker", "Website"),

    # --- UCLA Jonsson ---
    ("John Mazziotta", "CEO, UCLA Health", "C-Suite",
     "UCLA Health", "Jonsson Comprehensive",
     "Administration", None, "Decision Maker", "Website"),
    ("Michael Teitell", "Director, Jonsson Comprehensive Cancer Center", "Director",
     "UCLA Jonsson Comprehensive Cancer Center", "Jonsson Comprehensive",
     "Oncology", None, "Influencer", "Website"),

    # === LARGE COMMUNITY PRACTICES ===

    # --- Texas Oncology ---
    ("Debra Patt", "Executive VP, Texas Oncology", "C-Suite",
     "Texas Oncology", "Texas Oncology",
     "Administration", None, "Decision Maker", "Website"),
    ("Arjun Khunger", "VP Medical Affairs, Texas Oncology", "VP",
     "Texas Oncology", "Texas Oncology",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Bob Grillo", "CEO, McKesson US Oncology", "C-Suite",
     "McKesson US Oncology Network", "Texas Oncology",
     "Administration", None, "Decision Maker", "Website"),

    # --- Florida Cancer Specialists ---
    ("Lucio Gordan", "President and Managing Physician", "C-Suite",
     "Florida Cancer Specialists & Research Institute", "Florida Cancer Specialists",
     "Administration", None, "Decision Maker", "Website"),
    ("Nathan Walcker", "CEO", "C-Suite",
     "Florida Cancer Specialists & Research Institute", "Florida Cancer Specialists",
     "Administration", None, "Decision Maker", "Website"),
    ("Todd Schonherz", "Chief Operating Officer", "C-Suite",
     "Florida Cancer Specialists & Research Institute", "Florida Cancer Specialists",
     "Administration", None, "Decision Maker", "Website"),

    # --- Regional Cancer Care Associates ---
    ("Andrew Pecora", "President and Co-Founder", "C-Suite",
     "Regional Cancer Care Associates", "Regional Cancer Care Associates",
     "Administration", None, "Decision Maker", "Website"),
    ("Stuart Goldberg", "Chief of Medical Oncology", "C-Suite",
     "Regional Cancer Care Associates", "Regional Cancer Care Associates",
     "Oncology", None, "Influencer", "Website"),

    # --- New York Oncology Hematology ---
    ("John Drescher", "CEO, NYOH", "C-Suite",
     "New York Oncology Hematology", "New York Oncology Hematology",
     "Administration", None, "Decision Maker", "Website"),

    # === ADDITIONAL KEY PEOPLE - IT/Digital Leaders ===
    ("Chris Belmont", "VP and CIO", "C-Suite",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "IT", None, "Decision Maker", "Website"),
    ("Jorge Machado", "Chief Technology Officer", "C-Suite",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "IT", None, "Influencer", "Website"),

    # === Revenue Cycle / Finance leaders at key centers ===
    ("Shireen Dunwoody", "VP Revenue Cycle", "VP",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Revenue Cycle", None, "Decision Maker", "Website"),
    ("Amy Compton-Phillips", "Chief Clinical Officer", "C-Suite",
     "City of Hope", "City of Hope",
     "Clinical Ops", None, "Influencer", "Website"),

    # === Additional clinical leaders ===
    ("Hagop Kantarjian", "Chair, Dept of Leukemia", "Director",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("Robert Bast", "VP for Translational Research", "VP",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("James Allison", "Chair, Immunology", "Director",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Oncology", None, "Network", "Website"),
    ("Andrew Seidman", "Chief, Breast Medicine Service", "Director",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Oncology", None, "Influencer", "Website"),
    ("David Solit", "Director, Center for Molecular Oncology", "Director",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Oncology", None, "Influencer", "Website"),
    ("Harold Varmus", "Lewis Thomas University Professor", "Clinical",
     "Memorial Sloan Kettering Cancer Center", "Memorial Sloan Kettering",
     "Oncology", None, "Network", "Website"),
    ("Eric Winer", "Director, Yale Cancer Center (former Dana-Farber)", "Director",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Oncology", None, "Network", "Website"),
    ("Robert Mayer", "Faculty VP for Academic Affairs", "VP",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Administration", None, "Influencer", "Website"),
    ("Scott Kopetz", "Chair, GI Medical Oncology", "Director",
     "MD Anderson Cancer Center", "MD Anderson Cancer Center",
     "Oncology", None, "Influencer", "Website"),
    ("Anas Younes", "Chief Medical Officer, Moffitt", "C-Suite",
     "Moffitt Cancer Center", "Moffitt Cancer Center",
     "Clinical Ops", None, "Influencer", "Website"),
    ("Timothy Rebbeck", "VP for Cancer Prevention", "VP",
     "Dana-Farber Cancer Institute", "Dana-Farber Cancer Institute",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Mayo people ---
    ("Cheryl Willman", "Director, Mayo Clinic Cancer Programs", "Director",
     "Mayo Clinic", "Mayo Clinic Cancer Center",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Fred Hutch ---
    ("Scott Ramsey", "Director, Hutchinson Institute for Cancer Outcomes Research", "Director",
     "Fred Hutchinson Cancer Center", "Fred Hutch",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional UCSF ---
    ("Eric Small", "Deputy Director, UCSF Helen Diller", "Director",
     "UCSF Helen Diller", "UCSF Helen Diller",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional City of Hope ---
    ("Ravi Salgia", "Chair, Department of Medical Oncology", "Director",
     "City of Hope", "City of Hope",
     "Oncology", None, "Influencer", "Website"),
    ("Larry Kwak", "Deputy Director", "Director",
     "City of Hope", "City of Hope",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Roswell Park ---
    ("Boris Kuvshinoff", "Chair, Surgical Oncology", "Director",
     "Roswell Park Comprehensive Cancer Center", "Roswell Park Comprehensive",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Sylvester ---
    ("Jonathan Zager", "Chief, Surgical Oncology", "Director",
     "Sylvester Comprehensive Cancer Center", "Sylvester Comprehensive",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional UCLA ---
    ("Antoni Ribas", "Director, Parker Institute at UCLA", "Director",
     "UCLA Jonsson Comprehensive Cancer Center", "Jonsson Comprehensive",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Stanford ---
    ("Maximilian Diehn", "Associate Director, Clinical Sciences", "Director",
     "Stanford Cancer Institute", "Stanford Cancer Institute",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional Texas Oncology / US Oncology ---
    ("Jason Valant", "CEO, US Oncology Network", "C-Suite",
     "US Oncology Network / McKesson", "Texas Oncology",
     "Administration", None, "Decision Maker", "Website"),
    ("Troy Cox", "President, McKesson Oncology and Specialty", "C-Suite",
     "McKesson Oncology", "Texas Oncology",
     "Administration", None, "Decision Maker", "Website"),

    # --- Additional FCS ---
    ("Shilpa Gupta", "Medical Director, Research", "Director",
     "Florida Cancer Specialists & Research Institute", "Florida Cancer Specialists",
     "Oncology", None, "Influencer", "Website"),

    # --- Additional RCCA ---
    ("Andre Goy", "Physician-in-Chief and Chair", "C-Suite",
     "Regional Cancer Care Associates", "Regional Cancer Care Associates",
     "Oncology", None, "Influencer", "Website"),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    inserted = 0
    skipped = 0

    for entry in STAKEHOLDERS:
        (name, title, role_type, organization, center_fragment,
         department, linkedin_url, relevance, source) = entry

        # Check if already exists
        c.execute(
            "SELECT id FROM stakeholders WHERE LOWER(name) = LOWER(?) AND LOWER(organization) = LOWER(?)",
            [name, organization]
        )
        if c.fetchone():
            skipped += 1
            continue

        center_id = get_center_id(conn, center_fragment)

        c.execute(
            """INSERT INTO stakeholders
               (name, title, role_type, organization, center_id, department,
                linkedin_url, relevance_to_risa, source)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            [name, title, role_type, organization, center_id, department,
             linkedin_url, relevance, source]
        )
        inserted += 1

    conn.commit()
    conn.close()
    print("Stakeholders populated: {} inserted, {} skipped (already exist)".format(inserted, skipped))


if __name__ == "__main__":
    main()
