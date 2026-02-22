#!/usr/bin/env python3
"""Parse market-intelligence markdown files and populate SQLite database."""

import os
import re
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")

MD_FILES = [
    "cancer-centers-3-states.md",
    "us-oncology-market-map.md",
    "cancer-centers-research-report.md",
    "cancer-center-workflows.md",
    "risa-advisory-board-parker-classification.md",
    "us-oncology-whimsical-mindmap.md",
]


def create_tables(conn):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS cancer_centers")
    c.execute("DROP TABLE IF EXISTS market_segments")
    c.execute("DROP TABLE IF EXISTS key_organizations")
    c.execute("DROP TABLE IF EXISTS content_chunks")
    c.execute("DROP TABLE IF EXISTS content_chunks_fts")

    c.execute("""
        CREATE TABLE cancer_centers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            city TEXT,
            state TEXT,
            category TEXT,
            parent_org TEXT,
            est_oncologists TEXT,
            website TEXT,
            nci_type TEXT
        )
    """)
    c.execute("""
        CREATE TABLE market_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment_name TEXT,
            category TEXT,
            description TEXT,
            role TEXT,
            pain_points TEXT,
            risa_opportunity TEXT,
            money_flow TEXT,
            data_flow TEXT
        )
    """)
    c.execute("""
        CREATE TABLE key_organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            description TEXT,
            relevance_to_risa TEXT
        )
    """)
    c.execute("""
        CREATE TABLE content_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            section_heading TEXT,
            content_text TEXT,
            chunk_index INTEGER
        )
    """)
    c.execute("""
        CREATE VIRTUAL TABLE content_chunks_fts USING fts5(
            source_file, section_heading, content_text,
            content='content_chunks',
            content_rowid='id'
        )
    """)
    conn.commit()


def read_file(name):
    path = os.path.join(PARENT_DIR, name)
    if not os.path.exists(path):
        print("  Skipping (not found): {}".format(name))
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------- Cancer Centers Parser ----------

def detect_state(text_before):
    """Find which state section we're in based on preceding headings."""
    # Search backwards for state header
    m = re.search(r'#\s+(CALIFORNIA|TEXAS|WASHINGTON)\b', text_before, re.IGNORECASE)
    if m:
        return {"california": "CA", "texas": "TX", "washington": "WA"}[m.group(1).lower()]
    return ""


def parse_cancer_centers(content):
    """Parse all markdown tables from cancer-centers-3-states.md."""
    rows = []
    lines = content.split("\n")

    current_state = ""
    current_category = ""

    for i, line in enumerate(lines):
        # Detect state headers
        sm = re.match(r'^#\s+(CALIFORNIA|TEXAS|WASHINGTON)\s*$', line.strip(), re.IGNORECASE)
        if sm:
            current_state = {"california": "CA", "texas": "TX", "washington": "WA"}[sm.group(1).lower()]
            continue

        # Detect category headers like "## 1. NCI-Designated Cancer Centers (8)"
        cm = re.match(r'^##\s+\d+\.\s+(.+?)(?:\s*\(\d+\))?\s*$', line.strip())
        if cm:
            current_category = cm.group(1).strip()
            continue

        # Parse table rows (skip header/separator)
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]  # remove empty from leading/trailing |

        if len(cells) < 3:
            continue
        # Skip header rows and separator rows
        if cells[0] == "#" or re.match(r'^[-:]+$', cells[0]):
            continue
        # Skip non-numeric first column (header rows)
        if not re.match(r'^\d+$', cells[0]):
            continue

        # Different table formats based on category
        name = re.sub(r'\*\*', '', cells[1]).strip()
        city = cells[2] if len(cells) > 2 else ""

        nci_type = ""
        parent_org = ""
        est_onc = ""
        website = ""

        if "NCI" in current_category.upper():
            # NCI tables: #, Name, City, NCI Type, Parent, Est. Oncologists, Website
            nci_type = cells[3] if len(cells) > 3 else ""
            parent_org = cells[4] if len(cells) > 4 else ""
            est_onc = cells[5] if len(cells) > 5 else ""
            website = cells[6] if len(cells) > 6 else ""
        elif "Academic" in current_category:
            # Academic: #, Name, City, Parent, Est. Size, Website
            parent_org = cells[3] if len(cells) > 3 else ""
            est_onc = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Community" in current_category:
            # Community: #, Name, City/Region, Est. Size, Parent/Affiliation, Website
            est_onc = cells[3] if len(cells) > 3 else ""
            parent_org = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Hospital" in current_category:
            # Hospital: #, Name, City, Parent System, Est. Size, Website
            parent_org = cells[3] if len(cells) > 3 else ""
            est_onc = cells[4] if len(cells) > 4 else ""
            website = cells[5] if len(cells) > 5 else ""
        elif "Specialty" in current_category or "Boutique" in current_category:
            # Specialty: #, Name, City, Specialty, Notes, Website
            nci_type = cells[3] if len(cells) > 3 else ""  # store specialty in nci_type
            parent_org = cells[4] if len(cells) > 4 else ""  # notes as parent
            website = cells[5] if len(cells) > 5 else ""

        # Clean up
        est_onc = re.sub(r'\*\*', '', est_onc).strip()
        parent_org = re.sub(r'\*\*', '', parent_org).strip()
        website = re.sub(r'\*\*', '', website).strip()
        nci_type = re.sub(r'\*\*', '', nci_type).strip()

        rows.append((name, city, current_state, current_category, parent_org, est_onc, website, nci_type))

    return rows


# ---------- Market Segments Parser ----------

def parse_market_segments(content):
    """Parse us-oncology-market-map.md into segments."""
    segments = []
    # Split by ### headings (subsections)
    sections = re.split(r'^(##\s+.+)$', content, flags=re.MULTILINE)

    current_top_category = ""
    for i, section in enumerate(sections):
        top_match = re.match(r'^##\s+\d+\.\s+[^\n]*?([\w\s/&]+)', section)
        if top_match:
            current_top_category = top_match.group(0).strip().lstrip("# ").strip()
            continue

        # Find ### subsections
        subsections = re.split(r'^(###\s+.+)$', section, flags=re.MULTILINE)
        for j in range(len(subsections)):
            sub_match = re.match(r'^###\s+[\d.]+\s+(.+)', subsections[j])
            if sub_match and j + 1 < len(subsections):
                seg_name = sub_match.group(1).strip()
                body = subsections[j + 1]

                role = ""
                pain_points = ""
                risa_opp = ""
                money_flow = ""
                data_flow = ""
                description_parts = []

                for line in body.split("\n"):
                    line_s = line.strip().lstrip("- ")
                    if line_s.startswith("**Role:**"):
                        role = line_s.replace("**Role:**", "").strip()
                    elif line_s.startswith("**Pain Points:**"):
                        pain_points = line_s.replace("**Pain Points:**", "").strip()
                    elif line_s.startswith("**RISA Opportunity:**"):
                        risa_opp = line_s.replace("**RISA Opportunity:**", "").strip()
                    elif line_s.startswith("**Money Flow:**"):
                        money_flow = line_s.replace("**Money Flow:**", "").strip()
                    elif line_s.startswith("**Data Flow:**"):
                        data_flow = line_s.replace("**Data Flow:**", "").strip()
                    elif line_s.startswith("**Examples:**") or line_s.startswith("**"):
                        description_parts.append(line_s)

                desc = " ".join(description_parts)
                segments.append((seg_name, current_top_category, desc, role, pain_points, risa_opp, money_flow, data_flow))

    return segments


# ---------- Key Organizations Parser ----------

def parse_key_organizations(content):
    """Extract named organizations from the market map."""
    orgs = []
    seen = set()
    # Match lines like "- **Organization Name** — description"
    for m in re.finditer(r'[-*]\s+\*\*([^*]+)\*\*\s*[-—–]\s*(.+?)(?:\n|$)', content):
        name = m.group(1).strip()
        desc = m.group(2).strip()
        if name in seen or len(name) > 100:
            continue
        seen.add(name)

        org_type = "Unknown"
        name_lower = name.lower()
        if any(k in name_lower for k in ["pharma", "merck", "roche", "pfizer", "novartis", "lilly", "abbvie", "sanofi", "astrazeneca", "bms", "bristol", "johnson"]):
            org_type = "Pharma"
        elif any(k in name_lower for k in ["epic", "cerner", "oracle", "flatiron", "varian", "elekta", "waystar", "change", "availity"]):
            org_type = "Technology"
        elif any(k in name_lower for k in ["united", "aetna", "cigna", "elevance", "anthem", "blue cross", "humana", "medicare", "medicaid"]):
            org_type = "Payer"
        elif any(k in name_lower for k in ["fda", "cms", "nccn", "asco"]):
            org_type = "Regulatory/Guidelines"
        elif any(k in name_lower for k in ["tempus", "guardant", "foundation medicine", "myriad", "neogenomics", "natera"]):
            org_type = "Diagnostics"
        elif any(k in name_lower for k in ["mckesson", "cencora", "cardinal"]):
            org_type = "Distributor"
        else:
            org_type = "Other"

        risa_rel = ""
        if "risa" in desc.lower():
            risa_rel = desc

        orgs.append((name, org_type, desc, risa_rel))

    return orgs


# ---------- Content Chunks ----------

def chunk_text(text, max_words=500):
    """Split text into ~500-word chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks


def build_content_chunks(files_content):
    """Split all MD files into chunks by section."""
    all_chunks = []
    for fname, content in files_content:
        # Split by headings
        sections = re.split(r'^(#{1,3}\s+.+)$', content, flags=re.MULTILINE)
        current_heading = "Introduction"
        chunk_idx = 0
        for section in sections:
            heading_match = re.match(r'^#{1,3}\s+(.+)$', section.strip())
            if heading_match:
                current_heading = heading_match.group(1).strip()
                continue
            if len(section.strip()) < 20:
                continue
            for chunk in chunk_text(section.strip()):
                all_chunks.append((fname, current_heading, chunk, chunk_idx))
                chunk_idx += 1
    return all_chunks


def main():
    print("Building market intelligence database...")
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    c = conn.cursor()

    # 1. Cancer Centers
    content = read_file("cancer-centers-3-states.md")
    if content:
        rows = parse_cancer_centers(content)
        c.executemany(
            "INSERT INTO cancer_centers (name, city, state, category, parent_org, est_oncologists, website, nci_type) VALUES (?,?,?,?,?,?,?,?)",
            rows
        )
        print("  Inserted {} cancer centers".format(len(rows)))

    # 2. Market Segments
    content = read_file("us-oncology-market-map.md")
    if content:
        segs = parse_market_segments(content)
        c.executemany(
            "INSERT INTO market_segments (segment_name, category, description, role, pain_points, risa_opportunity, money_flow, data_flow) VALUES (?,?,?,?,?,?,?,?)",
            segs
        )
        print("  Inserted {} market segments".format(len(segs)))

        # 3. Key Organizations (from same file)
        orgs = parse_key_organizations(content)
        c.executemany(
            "INSERT INTO key_organizations (name, type, description, relevance_to_risa) VALUES (?,?,?,?)",
            orgs
        )
        print("  Inserted {} key organizations".format(len(orgs)))

    # 4. Content Chunks from all MD files
    files_content = []
    for fname in MD_FILES:
        fc = read_file(fname)
        if fc:
            files_content.append((fname, fc))
    chunks = build_content_chunks(files_content)
    c.executemany(
        "INSERT INTO content_chunks (source_file, section_heading, content_text, chunk_index) VALUES (?,?,?,?)",
        chunks
    )
    # Populate FTS index
    c.execute("""
        INSERT INTO content_chunks_fts (rowid, source_file, section_heading, content_text)
        SELECT id, source_file, section_heading, content_text FROM content_chunks
    """)
    print("  Inserted {} content chunks".format(len(chunks)))

    conn.commit()
    conn.close()
    print("Database built at: {}".format(DB_PATH))


if __name__ == "__main__":
    main()
