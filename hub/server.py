#!/usr/bin/env python3
"""FastAPI server for Market Intelligence Hub."""

import os
import sqlite3
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "market_intel.db")

app = FastAPI(title="RISA Labs Market Intelligence Hub")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- API Routes ---

@app.get("/api/centers")
def get_centers(
    state: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM cancer_centers WHERE 1=1"
    params = []  # type: List[Any]
    if state:
        query += " AND UPPER(state) = UPPER(?)"
        params.append(state)
    if category:
        query += " AND LOWER(category) LIKE LOWER(?)"
        params.append("%{}%".format(category))
    if search:
        query += " AND (LOWER(name) LIKE LOWER(?) OR LOWER(city) LIKE LOWER(?) OR LOWER(parent_org) LIKE LOWER(?))"
        params.extend(["%{}%".format(search)] * 3)
    query += " ORDER BY state, category, name"
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "centers": rows}


@app.get("/api/centers/geo")
def get_centers_geo():
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, city, state, category, est_oncologists, "
        "ehr_vendor, latitude, longitude, is_340b "
        "FROM cancer_centers WHERE latitude IS NOT NULL"
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "centers": rows}


@app.get("/api/centers/{center_id}")
def get_center(center_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM cancer_centers WHERE id = ?", [center_id])
    row = c.fetchone()
    conn.close()
    if not row:
        return JSONResponse({"error": "Not found"}, 404)
    return dict(row)


class NotesUpdate(BaseModel):
    notes: str


@app.put("/api/centers/{center_id}/notes")
def update_center_notes(center_id: int, req: NotesUpdate):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE cancer_centers SET notes = ? WHERE id = ?", [req.notes, center_id])
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True, "id": center_id}


@app.get("/api/segments")
def get_segments(search: Optional[str] = Query(None)):
    conn = get_db()
    c = conn.cursor()
    if search:
        c.execute(
            "SELECT * FROM market_segments WHERE LOWER(segment_name) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?) OR LOWER(role) LIKE LOWER(?) OR LOWER(pain_points) LIKE LOWER(?) OR LOWER(risa_opportunity) LIKE LOWER(?)",
            ["%{}%".format(search)] * 5
        )
    else:
        c.execute("SELECT * FROM market_segments ORDER BY category, segment_name")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "segments": rows}


@app.get("/api/organizations")
def get_organizations(type: Optional[str] = Query(None), search: Optional[str] = Query(None)):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM key_organizations WHERE 1=1"
    params = []  # type: List[Any]
    if type:
        query += " AND LOWER(type) = LOWER(?)"
        params.append(type)
    if search:
        query += " AND (LOWER(name) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        params.extend(["%{}%".format(search)] * 2)
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "organizations": rows}


@app.get("/api/organizations/{org_id}")
def get_organization(org_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM key_organizations WHERE id = ?", [org_id])
    row = c.fetchone()
    if not row:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    org = dict(row)
    # Get linked people count
    c.execute("SELECT COUNT(*) FROM stakeholders WHERE LOWER(organization) LIKE LOWER(?)", ["%{}%".format(org["name"])])
    org["people_count"] = c.fetchone()[0]
    # Get linked centers count
    c.execute("SELECT COUNT(*) FROM cancer_centers WHERE LOWER(parent_org) LIKE LOWER(?) OR LOWER(health_system) LIKE LOWER(?)",
              ["%{}%".format(org["name"]), "%{}%".format(org["name"])])
    org["centers_count"] = c.fetchone()[0]
    conn.close()
    return org


@app.put("/api/organizations/{org_id}/notes")
def update_org_notes(org_id: int, req: NotesUpdate):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE key_organizations SET notes = ? WHERE id = ?", [req.notes, org_id])
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True, "id": org_id}


@app.get("/api/search")
def search_content(q: str = Query(...)):
    conn = get_db()
    c = conn.cursor()
    # FTS5 search
    try:
        c.execute(
            """SELECT c.id, c.source_file, c.section_heading,
                      snippet(content_chunks_fts, 2, '<mark>', '</mark>', '...', 40) as snippet
               FROM content_chunks_fts fts
               JOIN content_chunks c ON c.id = fts.rowid
               WHERE content_chunks_fts MATCH ?
               ORDER BY rank
               LIMIT 20""",
            [q]
        )
        rows = [dict(r) for r in c.fetchall()]
    except Exception:
        # Fallback to LIKE search
        c.execute(
            """SELECT id, source_file, section_heading,
                      SUBSTR(content_text, 1, 300) as snippet
               FROM content_chunks
               WHERE LOWER(content_text) LIKE LOWER(?)
               LIMIT 20""",
            ["%{}%".format(q)]
        )
        rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "results": rows}


class StakeholderCreate(BaseModel):
    name: str
    title: Optional[str] = None
    role_type: Optional[str] = None
    organization: Optional[str] = None
    center_id: Optional[int] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    relevance_to_risa: Optional[str] = None
    source: Optional[str] = None
    last_contacted: Optional[str] = None
    next_followup: Optional[str] = None
    notes: Optional[str] = None


class StakeholderUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    role_type: Optional[str] = None
    organization: Optional[str] = None
    center_id: Optional[int] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    relevance_to_risa: Optional[str] = None
    source: Optional[str] = None
    last_contacted: Optional[str] = None
    next_followup: Optional[str] = None
    notes: Optional[str] = None


@app.get("/api/people/stats")
def get_people_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM stakeholders")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM stakeholders WHERE relevance_to_risa = 'Decision Maker'")
    decision_makers = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT center_id) FROM stakeholders WHERE center_id IS NOT NULL")
    centers_covered = c.fetchone()[0]
    c.execute("SELECT role_type, COUNT(*) as cnt FROM stakeholders GROUP BY role_type ORDER BY cnt DESC")
    by_role = [{"role_type": r["role_type"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT department, COUNT(*) as cnt FROM stakeholders GROUP BY department ORDER BY cnt DESC")
    by_dept = [{"department": r["department"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT relevance_to_risa, COUNT(*) as cnt FROM stakeholders GROUP BY relevance_to_risa ORDER BY cnt DESC")
    by_rel = [{"relevance": r["relevance_to_risa"], "count": r["cnt"]} for r in c.fetchall()]
    conn.close()
    return {"total": total, "decision_makers": decision_makers, "centers_covered": centers_covered,
            "by_role": by_role, "by_department": by_dept, "by_relevance": by_rel}


@app.get("/api/people")
def get_people(
    role_type: Optional[str] = Query(None),
    organization: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    center_id: Optional[int] = Query(None),
    relevance: Optional[str] = Query(None),
):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM stakeholders WHERE 1=1"
    params = []  # type: List[Any]
    if role_type:
        query += " AND role_type = ?"
        params.append(role_type)
    if organization:
        query += " AND LOWER(organization) LIKE LOWER(?)"
        params.append("%{}%".format(organization))
    if department:
        query += " AND department = ?"
        params.append(department)
    if relevance:
        query += " AND relevance_to_risa = ?"
        params.append(relevance)
    if center_id is not None:
        query += " AND center_id = ?"
        params.append(center_id)
    if search:
        query += " AND (LOWER(name) LIKE LOWER(?) OR LOWER(title) LIKE LOWER(?) OR LOWER(organization) LIKE LOWER(?))"
        params.extend(["%{}%".format(search)] * 3)
    query += " ORDER BY name"
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "people": rows}


@app.get("/api/people/{person_id}")
def get_person(person_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM stakeholders WHERE id = ?", [person_id])
    row = c.fetchone()
    conn.close()
    if not row:
        return JSONResponse({"error": "Not found"}, 404)
    return dict(row)


@app.post("/api/people")
def create_person(req: StakeholderCreate):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """INSERT INTO stakeholders (name, title, role_type, organization, center_id, department,
           email, phone, linkedin_url, relevance_to_risa, source, last_contacted, next_followup, notes)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        [req.name, req.title, req.role_type, req.organization, req.center_id, req.department,
         req.email, req.phone, req.linkedin_url, req.relevance_to_risa, req.source,
         req.last_contacted, req.next_followup, req.notes]
    )
    conn.commit()
    pid = c.lastrowid
    conn.close()
    return {"ok": True, "id": pid}


@app.put("/api/people/{person_id}")
def update_person(person_id: int, req: StakeholderUpdate):
    conn = get_db()
    c = conn.cursor()
    fields = []
    params = []  # type: List[Any]
    data = req.dict(exclude_unset=True)
    for key, val in data.items():
        fields.append("{} = ?".format(key))
        params.append(val)
    if not fields:
        conn.close()
        return JSONResponse({"error": "No fields to update"}, 400)
    fields.append("updated_at = datetime('now')")
    params.append(person_id)
    c.execute("UPDATE stakeholders SET {} WHERE id = ?".format(", ".join(fields)), params)
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True, "id": person_id}


@app.delete("/api/people/{person_id}")
def delete_person(person_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM stakeholders WHERE id = ?", [person_id])
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True}


# --- Workflow API Routes ---

@app.get("/api/workflows")
def get_workflows(
    department: Optional[str] = Query(None),
    stage: Optional[int] = Query(None),
    center: Optional[str] = Query(None),
    complexity: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_bottleneck: Optional[int] = Query(None),
):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM workflows WHERE 1=1"
    params = []  # type: List[Any]
    if department:
        query += " AND LOWER(department) = LOWER(?)"
        params.append(department)
    if stage is not None:
        query += " AND patient_journey_stage = ?"
        params.append(stage)
    if center:
        query += " AND centers_applicable LIKE ?"
        params.append("%{}%".format(center))
    if complexity:
        query += " AND LOWER(complexity) = LOWER(?)"
        params.append(complexity)
    if min_bottleneck is not None:
        query += " AND bottleneck_severity >= ?"
        params.append(min_bottleneck)
    if search:
        query += " AND (LOWER(name) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?) OR LOWER(pain_points) LIKE LOWER(?) OR LOWER(risa_opportunity) LIKE LOWER(?))"
        params.extend(["%{}%".format(search)] * 4)
    query += " ORDER BY workflow_id"
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"count": len(rows), "workflows": rows}


@app.get("/api/workflows/stats")
def get_workflow_stats():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM workflows")
    total = c.fetchone()[0]
    c.execute("SELECT department, COUNT(*) as cnt FROM workflows GROUP BY department ORDER BY cnt DESC")
    by_dept = [{"department": r["department"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT patient_journey_stage, stage_name, COUNT(*) as cnt FROM workflows GROUP BY patient_journey_stage ORDER BY patient_journey_stage")
    by_stage = [{"stage": r["patient_journey_stage"], "stage_name": r["stage_name"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT complexity, COUNT(*) as cnt FROM workflows GROUP BY complexity ORDER BY cnt DESC")
    by_complexity = [{"complexity": r["complexity"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT centers_applicable, COUNT(*) as cnt FROM workflows GROUP BY centers_applicable ORDER BY cnt DESC")
    by_center = [{"centers": r["centers_applicable"], "count": r["cnt"]} for r in c.fetchall()]
    c.execute("SELECT AVG(bottleneck_severity) as avg_bn, AVG(avg_time_minutes) as avg_time FROM workflows")
    avgs = c.fetchone()
    c.execute("SELECT COUNT(*) FROM workflow_steps")
    total_steps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM workflow_steps WHERE is_automatable = 1")
    automatable_steps = c.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "total_steps": total_steps,
        "automatable_steps": automatable_steps,
        "automation_pct": round(automatable_steps * 100.0 / total_steps, 1) if total_steps else 0,
        "avg_bottleneck": round(avgs["avg_bn"], 1) if avgs["avg_bn"] else 0,
        "avg_time_minutes": round(avgs["avg_time"], 0) if avgs["avg_time"] else 0,
        "by_department": by_dept,
        "by_stage": by_stage,
        "by_complexity": by_complexity,
        "by_center": by_center,
    }


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    conn = get_db()
    c = conn.cursor()
    # Support both numeric id and WF### format
    if workflow_id.startswith("WF"):
        c.execute("SELECT * FROM workflows WHERE workflow_id = ?", [workflow_id])
    else:
        c.execute("SELECT * FROM workflows WHERE id = ?", [int(workflow_id)])
    row = c.fetchone()
    if not row:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    wf = dict(row)
    # Get steps
    c.execute("SELECT * FROM workflow_steps WHERE workflow_id = ? ORDER BY step_number", [wf["id"]])
    wf["steps"] = [dict(r) for r in c.fetchall()]
    # Get stakeholders
    c.execute("SELECT * FROM workflow_stakeholders WHERE workflow_id = ?", [wf["id"]])
    wf["stakeholders"] = [dict(r) for r in c.fetchall()]
    conn.close()
    return wf


@app.put("/api/workflows/{workflow_id}/notes")
def update_workflow_notes(workflow_id: str, req: NotesUpdate):
    conn = get_db()
    c = conn.cursor()
    if workflow_id.startswith("WF"):
        c.execute("UPDATE workflows SET notes = ? WHERE workflow_id = ?", [req.notes, workflow_id])
    else:
        c.execute("UPDATE workflows SET notes = ? WHERE id = ?", [req.notes, int(workflow_id)])
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True}


class WorkflowNotesUpdate(BaseModel):
    notes: str


@app.put("/api/workflows/{workflow_id}/notes")
def update_workflow_notes(workflow_id: str, req: WorkflowNotesUpdate):
    conn = get_db()
    c = conn.cursor()
    if workflow_id.startswith("WF"):
        c.execute("UPDATE workflows SET notes = ? WHERE workflow_id = ?", [req.notes, workflow_id])
    else:
        c.execute("UPDATE workflows SET notes = ? WHERE id = ?", [req.notes, int(workflow_id)])
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return JSONResponse({"error": "Not found"}, 404)
    conn.close()
    return {"ok": True}


class ChatRequest(BaseModel):
    question: str


@app.post("/api/chat")
def chat(req: ChatRequest):
    question = req.question
    conn = get_db()
    c = conn.cursor()

    # Gather context from multiple sources
    context_parts = []

    # FTS search
    try:
        # Build a simple query from keywords
        words = [w for w in question.split() if len(w) > 2]
        fts_query = " OR ".join(words) if words else question
        c.execute(
            """SELECT c.source_file, c.section_heading, c.content_text
               FROM content_chunks_fts fts
               JOIN content_chunks c ON c.id = fts.rowid
               WHERE content_chunks_fts MATCH ?
               ORDER BY rank
               LIMIT 8""",
            [fts_query]
        )
        for r in c.fetchall():
            context_parts.append("[Source: {} | Section: {}]\n{}".format(r[0], r[1], r[2][:800]))
    except Exception:
        pass

    # Also search centers if relevant
    for kw in ["center", "cancer", "hospital", "oncolog", "NCI", "community", "academic"]:
        if kw.lower() in question.lower():
            c.execute("SELECT name, city, state, category, parent_org, est_oncologists FROM cancer_centers LIMIT 20")
            centers = c.fetchall()
            if centers:
                center_text = "\n".join(
                    "{} | {} | {} | {} | {} | {}".format(*row) for row in centers[:15]
                )
                context_parts.append("[Cancer Centers Data]\n" + center_text)
            break

    # Search segments if relevant
    for kw in ["market", "segment", "payer", "pharma", "risa", "opportunity", "RCM", "billing"]:
        if kw.lower() in question.lower():
            c.execute("SELECT segment_name, category, role, pain_points, risa_opportunity FROM market_segments")
            segs = c.fetchall()
            if segs:
                seg_text = "\n".join(
                    "{} | {} | {} | {} | {}".format(*row) for row in segs[:10]
                )
                context_parts.append("[Market Segments Data]\n" + seg_text)
            break

    conn.close()

    context = "\n\n---\n\n".join(context_parts) if context_parts else "No relevant context found."

    has_local = context != "No relevant context found."

    # Try Claude API
    try:
        import anthropic
        client = anthropic.Anthropic()

        base_context = (
            "You are a market intelligence analyst for RISA Labs, an oncology healthcare AI company. "
            "You are embedded in RISA's Market Intelligence Hub - a local web app at localhost:8501. "
            "The hub contains: Cancer Centers database (303 centers across CA, TX, WA, FL, NY, MA), "
            "Market Map (43 segments), Organizations directory (126 orgs), People/Stakeholder directory, "
            "and interactive visualizations. "
            "Available visualizations in the hub: "
            "1) Oncology Money Flows (/viz/oncology-money-flows.html) - financial interactions with cancer care providers, "
            "2) Oncology Workflows (/viz/oncology-workflows.html) - 120 workflows across cancer centers, "
            "3) Cancer Centers Map (/viz/cancer-centers.html) - geographic visualization, "
            "4) US Oncology Mind Map (/viz/us-oncology-mindmap.html) - ecosystem mind map. "
            "You CANNOT access URLs or browse websites. If a user shares a URL, acknowledge you can't visit it "
            "but answer based on what you know about that content from the hub's database. "
            "Do NOT use em dashes. Use hyphens instead. "
        )
        if has_local:
            system_prompt = base_context + (
                "Answer the question using the provided internal database context. "
                "Also use your general knowledge to supplement and enrich the answer where helpful "
                "(e.g. EHR vendors, payer details, industry facts). "
                "Clearly distinguish between what comes from internal data vs your general knowledge. "
                "Be concise, specific. Format with markdown."
            )
        else:
            system_prompt = base_context + (
                "The internal database did not have relevant results for this query. "
                "Use your general knowledge about oncology, healthcare, and the US cancer care market "
                "to provide a helpful, accurate answer. Note that this is from general knowledge, "
                "not RISA's internal data. Be concise, specific. Format with markdown."
            )

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": "Internal database context:\n{}\n\nQuestion: {}".format(context, question)
            }]
        )
        answer = response.content[0].text
        mode = "ai+local" if has_local else "ai+general"
        return {"answer": answer, "sources": [p[:100] for p in context_parts], "mode": mode}
    except Exception as e:
        # Fallback: return raw search results
        fallback_parts = context_parts[:]
        return {
            "answer": "**Search Results for: {}**\n\n{}".format(
                question,
                "\n\n".join("• " + p[:500] for p in fallback_parts[:5]) if fallback_parts else "No results found."
            ),
            "sources": [p[:100] for p in context_parts],
            "mode": "search-fallback",
            "note": "LLM unavailable ({}). Showing raw search results.".format(str(e)[:80])
        }


# --- Serve existing HTML visualizations ---

@app.get("/viz/{filename}")
def serve_viz(filename: str):
    import re
    from fastapi.responses import HTMLResponse
    path = os.path.join(PARENT_DIR, filename)
    if os.path.exists(path) and filename.endswith(".html"):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        back_btn = ('<a href="/" style="position:fixed;top:16px;left:16px;z-index:99999;'
                    'background:#6c5ce7;color:#fff;padding:8px 18px;border-radius:8px;'
                    'text-decoration:none;font-family:system-ui;font-size:14px;'
                    'font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.3);">'
                    '&#8592; Hub</a>')
        content = re.sub(r'(<body[^>]*>)', r'\1' + back_btn, content, count=1)
        return HTMLResponse(content)
    return JSONResponse({"error": "Not found"}, 404)


# --- Serve static hub files ---

@app.get("/")
def serve_index():
    from fastapi.responses import HTMLResponse
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content, headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"})


@app.get("/hub/{filepath:path}")
def serve_hub_static(filepath: str):
    path = os.path.join(BASE_DIR, filepath)
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"error": "Not found"}, 404)
