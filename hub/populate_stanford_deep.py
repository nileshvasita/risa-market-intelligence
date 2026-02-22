#!/usr/bin/env python3
"""Deep populate Stanford Cancer Institute / Stanford Health Care stakeholders."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_intel.db")
CENTER_ID = 2  # Stanford Cancer Institute

STAKEHOLDERS = [
    # ===================== TIER 1: EXECUTIVE LEADERSHIP =====================
    {
        "name": "Steven Artandi",
        "title": "Director, Stanford Cancer Institute; Senior Associate Dean for Cancer Programs; Chief Cancer Officer, Stanford Health Care",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Cancer Institute Leadership",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "MD, PhD. Replaced Beverly Mitchell as SCI Director. Also Senior Associate Dean for Cancer Programs at Stanford Medicine. Telomere biology researcher. Key decision maker for all cancer institute strategy.",
    },
    {
        "name": "Michael Kenney",
        "title": "Assistant Dean; Deputy Director of Administration, Stanford Cancer Institute",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Cancer Institute Administration",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "Oversees administrative operations of Stanford Cancer Institute. Key contact for operational and financial decisions.",
    },
    {
        "name": "David Entwistle",
        "title": "President and Chief Executive Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Executive Leadership",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "Top executive at Stanford Health Care. Ultimate decision maker for major technology and operational investments across the health system.",
    },
    {
        "name": "Linda Hoff",
        "title": "Executive Vice President, Chief Financial Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Finance",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "CFO overseeing all financial operations. Key decision maker for revenue cycle technology investments and financial strategy.",
    },
    {
        "name": "Rick Shumway",
        "title": "Executive Vice President, Chief Operating Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Operations",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "COO responsible for operational excellence across Stanford Health Care.",
    },
    {
        "name": "Niraj Sehgal",
        "title": "Executive Vice President and Chief Physician Executive, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Medical Affairs",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "MD, MPH. Chief Physician Executive overseeing medical staff and clinical quality. Influential in clinical workflow and technology adoption decisions.",
    },
    {
        "name": "Tip Kim",
        "title": "Executive Vice President, Chief Market Development Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Market Development",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Leads market development and growth strategy for Stanford Health Care.",
    },
    {
        "name": "Priya Singh",
        "title": "Executive Vice President, Chief Strategy Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Strategy",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "Chief Strategy Officer. Oversees strategic planning and partnerships. Key contact for strategic technology partnerships.",
    },
    {
        "name": "Michael Pfeffer",
        "title": "Senior Vice President, Chief Information Officer, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Information Technology",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "MD. CIO responsible for all IT systems including EHR/Epic, clinical informatics, and digital health. Primary decision maker for health IT investments and integrations.",
    },

    # ===================== TIER 1B: SENIOR LEADERSHIP =====================
    {
        "name": "Jill Buathier",
        "title": "Senior Vice President, Chief Revenue Cycle Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Revenue Cycle",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "Chief Revenue Cycle Officer. Directly oversees billing, coding, prior authorization, claims, and revenue cycle operations. PRIMARY target for RISA -- owns the revenue cycle function.",
    },
    {
        "name": "Ted Ross",
        "title": "Senior Vice President, Finance, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Finance",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "SVP Finance working alongside CFO Linda Hoff. Key stakeholder for financial technology and revenue optimization decisions.",
    },
    {
        "name": "James Martin Jr.",
        "title": "Senior Vice President, Controller, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Finance / Accounting",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Controller overseeing accounting and financial reporting. Relevant for revenue cycle financial reporting and analytics.",
    },
    {
        "name": "Timothy Seay-Morrison",
        "title": "Senior Vice President, Cancer Services, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Cancer Services",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "SVP Cancer Services. Directly oversees cancer service line operations. Critical decision maker for oncology-specific operational technology and workflows.",
    },
    {
        "name": "Alison Kerr",
        "title": "Senior Vice President, Destination Service Lines and Chief Clinical Operations Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Clinical Operations",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "Chief Clinical Operations Officer overseeing destination service lines. Influential in operational workflow and technology decisions for specialty care.",
    },
    {
        "name": "Alpa Vyas",
        "title": "Senior Vice President, Chief Patient Experience and Operational Performance Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Patient Experience / Operations",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Oversees patient experience and operational performance. Relevant for patient access and scheduling technology.",
    },
    {
        "name": "Neera Ahuja",
        "title": "Senior Vice President and Chief Medical Officer, Inpatient Care, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Medical Affairs - Inpatient",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. CMO for Inpatient Care. Oversees inpatient clinical quality and medical staff affairs.",
    },
    {
        "name": "Dale Beatty",
        "title": "Senior Vice President, Patient Care Services, and Chief Nursing Executive, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Nursing",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Chief Nursing Executive. Oversees all nursing operations including oncology nursing and infusion services.",
    },
    {
        "name": "Jennie Crews",
        "title": "President and CEO Stanford Medicine Partners; CMO Ambulatory Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Ambulatory Care",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Leads Stanford Medicine Partners network and ambulatory care. Relevant for outpatient oncology care delivery.",
    },
    {
        "name": "Dawn Rorig",
        "title": "Senior Vice President, Chief Human Resources Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Human Resources",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "CHRO overseeing workforce strategy and HR operations.",
    },
    {
        "name": "Cheryl Wagonhurst",
        "title": "Senior Vice President, Chief Compliance Officer and Privacy Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Compliance",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Chief Compliance and Privacy Officer. Relevant for compliance aspects of revenue cycle and AI-based solutions.",
    },
    {
        "name": "Michiko Tanabe",
        "title": "Senior Vice President, Chief Marketing Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Marketing",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "CMO for marketing and communications.",
    },
    {
        "name": "Ruch Kumbhani",
        "title": "Interim Senior Vice President, Ambulatory Care Operations and Service Lines, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Ambulatory Operations",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Interim SVP for ambulatory care operations. Oversees outpatient service line operations including cancer center clinic operations.",
    },
    {
        "name": "Paul Maggio",
        "title": "Senior Vice President, Chief Quality Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Quality",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Chief Quality Officer overseeing quality improvement and safety programs.",
    },
    {
        "name": "Mariah Bianchi",
        "title": "Senior Vice President, Quality, Safety, and Clinical Effectiveness, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Quality and Safety",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Oversees quality, safety, and clinical effectiveness programs.",
    },
    {
        "name": "Sam Wald",
        "title": "Chief Medical Officer, Perioperative and Interventional Care, Stanford Health Care",
        "role_type": "C-Suite",
        "organization": "Stanford Health Care",
        "department": "Perioperative Care",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. CMO for perioperative and interventional care. Relevant for surgical oncology operations.",
    },
    {
        "name": "Joyce Sackey",
        "title": "Chief Community Engagement Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Community Engagement",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "MD. Leads community engagement and health equity initiatives.",
    },
    {
        "name": "Amanda Chawla",
        "title": "Senior Vice President, Chief Supply Chain Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Supply Chain",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "Chief Supply Chain Officer overseeing procurement and supply chain operations.",
    },
    {
        "name": "Elaine Ziemba",
        "title": "Senior Vice President, Chief Risk/Admin Officer, Stanford Health Care",
        "role_type": "VP",
        "organization": "Stanford Health Care",
        "department": "Risk Management",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "Chief Risk and Administrative Officer.",
    },

    # ===================== TIER 2: ONCOLOGY DIVISION LEADERSHIP =====================
    {
        "name": "Heather Wakelee",
        "title": "Chief, Division of Oncology, Stanford Medicine",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Winston Chen and Phyllis Huang Professor. Chief of the Division of Oncology. Lung cancer specialist. Key clinical influencer for oncology workflows and technology adoption.",
    },
    {
        "name": "Allison Kurian",
        "title": "Associate Division Chief of Academic Affairs, Division of Oncology",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD, MSc. Professor of Medicine (Oncology) and of Epidemiology and Population Health. Expert in breast cancer genetics and population-level cancer research.",
    },
    {
        "name": "Dean Felsher",
        "title": "Associate Division Chief of Scientific Affairs, Division of Oncology",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD, PhD. Professor of Medicine - Oncology. Pioneer in oncogene addiction research. Leads scientific affairs for the oncology division.",
    },
    {
        "name": "Shagufta Shaheen",
        "title": "Associate Division Chief for Culture and Community, Division of Oncology",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Clinical Assistant Professor, Medicine - Oncology. Also Oncology Section Chief at Palo Alto VA. (Note: website lists her and Millie Das in separate roles.)",
    },
    {
        "name": "Millie Das",
        "title": "Oncology Section Chief, Palo Alto Veterans Administration Health Care System",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Clinical Professor, Medicine - Oncology. Section Chief for oncology at Palo Alto VA. Lung cancer researcher.",
    },
    {
        "name": "Kavitha Ramchandran",
        "title": "Associate Division Chief for Mentorship and Career Development, Division of Oncology",
        "role_type": "Division Chief",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Clinical Professor, Medicine - Oncology. Expert in supportive and palliative care in oncology. Leads mentorship programs.",
    },
    {
        "name": "Tyler Johnson",
        "title": "Medical Oncology Fellowship Director, Division of Oncology",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology Education",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "MD. Clinical Associate Professor, Medicine - Oncology. Directs the medical oncology fellowship training program.",
    },

    # ===================== TIER 2B: SCI ASSOCIATE DIRECTORS =====================
    {
        "name": "Mark Pegram",
        "title": "Associate Director of Clinical Research, Stanford Cancer Institute",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Clinical Research",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Suzy Yuan-Huey Hung Endowed Professor of Medical Oncology. Also Associate Dean for Clinical Research Quality. Medical Director of clinical trials. HER2-targeted therapy pioneer. Key influencer for clinical trial operations and research workflows.",
    },
    {
        "name": "Melinda Telli",
        "title": "Director, Breast Cancer Program, Stanford Cancer Institute; Associate Director of Clinical Research",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Breast Cancer Program",
        "relevance_to_risa": "Influencer",
        "source": "LinkedIn",
        "linkedin_url": "https://www.linkedin.com/in/melinda-telli-180620b",
        "notes": "MD. Professor of Medicine. Leads the Breast Cancer Program at SCI. Research focuses on triple-negative and hereditary breast cancer. Also Associate Director of the Stanford Women's Cancer Center.",
    },
    {
        "name": "Rondeep Brar",
        "title": "Associate Director for Clinical Care, Stanford Cancer Institute; Medical Director, Cancer Destination Service Line",
        "role_type": "Director",
        "organization": "Stanford Cancer Institute",
        "department": "Clinical Care",
        "relevance_to_risa": "Decision Maker",
        "source": "Website",
        "notes": "MD. Clinical Associate Professor of Medicine. Dual role as SCI Associate Director for Clinical Care and SHC Medical Director for Cancer DSL. Key bridge between academic cancer institute and health system operations.",
    },

    # ===================== TIER 2C: SCI SENIOR ADVISORS =====================
    {
        "name": "Jonathan Berek",
        "title": "Senior Advisor, Stanford Cancer Institute",
        "role_type": "Advisor",
        "organization": "Stanford Cancer Institute",
        "department": "Gynecologic Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD, MMS. Director of Stanford Women's Cancer Center. Laurie Kraus Lacob Professor. Leading gynecologic oncologist. Former SCI leadership.",
    },
    {
        "name": "George Fisher",
        "title": "Senior Advisor, Stanford Cancer Institute",
        "role_type": "Advisor",
        "organization": "Stanford Cancer Institute",
        "department": "Medical Oncology",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD, PhD. Professor of Medicine. GI oncology expert. Senior advisor to SCI leadership.",
    },
    {
        "name": "Robert Negrin",
        "title": "Senior Advisor, Stanford Cancer Institute",
        "role_type": "Advisor",
        "organization": "Stanford Cancer Institute",
        "department": "Blood and Marrow Transplant",
        "relevance_to_risa": "Influencer",
        "source": "Website",
        "notes": "MD. Professor of Medicine. Expert in blood and marrow transplantation. Former Division Chief of BMT. Senior advisor to SCI.",
    },
    {
        "name": "Irving Weissman",
        "title": "Senior Advisor, Stanford Cancer Institute",
        "role_type": "Advisor",
        "organization": "Stanford Cancer Institute",
        "department": "Stem Cell Biology",
        "relevance_to_risa": "Other",
        "source": "Website",
        "notes": "MD. Director of Stanford Institute for Stem Cell Biology. Pioneer in stem cell research and cancer stem cell biology. National Academy of Sciences member.",
    },
]

def upsert_stakeholder(cursor, s):
    """Insert or update a stakeholder. Skip if name+org exists with same title."""
    cursor.execute(
        "SELECT id, title FROM stakeholders WHERE name = ? AND organization = ?",
        (s["name"], s["organization"])
    )
    existing = cursor.fetchone()
    
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    if existing:
        # Update existing record
        cursor.execute("""
            UPDATE stakeholders SET
                title = ?,
                role_type = ?,
                center_id = ?,
                department = ?,
                relevance_to_risa = ?,
                source = ?,
                notes = ?,
                linkedin_url = COALESCE(?, linkedin_url),
                updated_at = ?
            WHERE id = ?
        """, (
            s["title"],
            s["role_type"],
            CENTER_ID,
            s.get("department", ""),
            s["relevance_to_risa"],
            s["source"],
            s["notes"],
            s.get("linkedin_url"),
            now,
            existing[0],
        ))
        print(f"  Updated: {s['name']} (id={existing[0]})")
    else:
        cursor.execute("""
            INSERT INTO stakeholders (
                name, title, role_type, organization, center_id, department,
                relevance_to_risa, source, notes, linkedin_url, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s["name"],
            s["title"],
            s["role_type"],
            s["organization"],
            CENTER_ID,
            s.get("department", ""),
            s["relevance_to_risa"],
            s["source"],
            s["notes"],
            s.get("linkedin_url"),
            now,
            now,
        ))
        print(f"  Inserted: {s['name']}")


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Processing {len(STAKEHOLDERS)} stakeholders for Stanford Cancer Institute (center_id={CENTER_ID})...")
    
    for s in STAKEHOLDERS:
        upsert_stakeholder(cursor, s)
    
    conn.commit()
    
    # Summary
    cursor.execute("SELECT COUNT(*) FROM stakeholders WHERE organization LIKE '%Stanford%'")
    total = cursor.fetchone()[0]
    print(f"\nDone. Total Stanford stakeholders in DB: {total}")
    
    # Breakdown by relevance
    cursor.execute("""
        SELECT relevance_to_risa, COUNT(*) FROM stakeholders 
        WHERE organization LIKE '%Stanford%' 
        GROUP BY relevance_to_risa ORDER BY COUNT(*) DESC
    """)
    print("\nBy relevance to RISA:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    conn.close()


if __name__ == "__main__":
    main()
