#!/usr/bin/env python3
"""
Master rebuild script - rebuilds the entire market_intel.db from scratch.
Run this to recreate the database from source data + scripts.

Usage: python3 rebuild_all.py
"""

import os
import sys
import subprocess
import sqlite3
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")

def run_script(name, description):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        print(f"  SKIP {name} - file not found")
        return False
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"  Running: {name}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, path],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )
    if result.stdout:
        # Indent output
        for line in result.stdout.strip().split('\n'):
            print(f"  {line}")
    if result.returncode != 0:
        print(f"  ERROR: {name} failed with code {result.returncode}")
        if result.stderr:
            for line in result.stderr.strip().split('\n')[:10]:
                print(f"  {line}")
        return False
    return True


def add_health_systems():
    """Add health systems from cancer_centers parent_org to key_organizations."""
    print(f"\n{'='*60}")
    print(f"  Adding health systems to organizations directory")
    print(f"{'='*60}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ensure notes column exists on key_organizations
    try:
        c.execute("ALTER TABLE key_organizations ADD COLUMN notes TEXT")
    except Exception:
        pass  # Column already exists
    
    skip_names = {
        '10+ locations', 'Acquired by Cedars-Sinai', 'Boutique practice',
        'Independent', 'Physician-owned', 'N/A', '', None
    }
    
    c.execute('''
        SELECT parent_org, COUNT(*) as cnt, GROUP_CONCAT(DISTINCT state) as states
        FROM cancer_centers 
        WHERE parent_org IS NOT NULL AND parent_org != ''
        AND parent_org NOT IN (SELECT name FROM key_organizations)
        GROUP BY parent_org
        HAVING cnt >= 1
        ORDER BY cnt DESC
    ''')
    rows = c.fetchall()
    
    inserted = 0
    for name, cnt, states in rows:
        if name in skip_names:
            continue
        c.execute(
            '''INSERT OR IGNORE INTO key_organizations (name, type, description)
               VALUES (?, 'Health System', ?)''',
            [name, "Health system with {} cancer center(s) in {}".format(cnt, states)]
        )
        inserted += c.rowcount
    
    conn.commit()
    conn.close()
    print(f"  Inserted {inserted} health systems into organizations")


def print_summary():
    """Print database summary."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"\n{'='*60}")
    print(f"  DATABASE SUMMARY")
    print(f"{'='*60}")
    
    tables = [
        ("cancer_centers", "Cancer Centers"),
        ("market_segments", "Market Segments"),
        ("key_organizations", "Organizations"),
        ("content_chunks", "Content Chunks"),
        ("stakeholders", "Stakeholders"),
        ("workflows", "Workflows"),
        ("workflow_steps", "Workflow Steps"),
        ("workflow_stakeholders", "Workflow Stakeholders"),
    ]
    
    for table, label in tables:
        try:
            c.execute("SELECT COUNT(*) FROM {}".format(table))
            count = c.fetchone()[0]
            print(f"  {label:.<30} {count:>6}")
        except Exception:
            print(f"  {label:.<30} {'N/A':>6}")
    
    # State breakdown
    try:
        c.execute("SELECT state, COUNT(*) FROM cancer_centers GROUP BY state ORDER BY COUNT(*) DESC")
        states = c.fetchall()
        print(f"\n  Centers by state: {', '.join('{} ({})'.format(s, c) for s, c in states)}")
    except Exception:
        pass
    
    conn.close()
    print(f"\n  Database: {DB_PATH}")
    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"  Size: {size_mb:.1f} MB")


def main():
    start = time.time()
    
    print("\n" + "#"*60)
    print("#  RISA Market Intelligence - Full Database Rebuild")
    print("#"*60)
    
    # Remove existing DB for clean rebuild
    if os.path.exists(DB_PATH):
        print(f"\n  Removing existing database...")
        os.remove(DB_PATH)
    
    # Step 1: Base tables + content from markdown
    run_script("build_db.py", "Step 1/8: Building base tables + content chunks")
    
    # Step 2: Add FL, NY, MA centers
    run_script("add_new_states.py", "Step 2/8: Adding FL, NY, MA cancer centers")
    
    # Step 3: Enrich centers (EHR, beds, 340B)
    run_script("enrich_centers.py", "Step 3/8: Enriching center data (EHR, beds, 340B)")
    
    # Step 4: Geocode centers
    run_script("geocode_centers.py", "Step 4/8: Geocoding cancer centers")
    
    # Step 5: Import workflows
    run_script("import_workflows.py", "Step 5/8: Importing workflows + steps + stakeholders")
    
    # Step 6: Populate stakeholders (initial 85)
    run_script("populate_stakeholders.py", "Step 6/8: Populating initial stakeholders")
    
    # Step 7: Stanford deep-dive (45 people)
    run_script("populate_stanford_deep.py", "Step 7/8: Stanford leadership deep-dive")
    
    # Step 8: Add health systems to orgs
    add_health_systems()
    
    # Summary
    print_summary()
    
    elapsed = time.time() - start
    print(f"\n  Rebuild completed in {elapsed:.1f}s")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
