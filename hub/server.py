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

        if has_local:
            system_prompt = (
                "You are a market intelligence analyst for RISA Labs, an oncology healthcare AI company. "
                "Answer the question using the provided internal database context. "
                "Also use your general knowledge to supplement and enrich the answer where helpful "
                "(e.g. EHR vendors, payer details, industry facts). "
                "Clearly distinguish between what comes from internal data vs your general knowledge. "
                "Be concise, specific. Format with markdown."
            )
        else:
            system_prompt = (
                "You are a market intelligence analyst for RISA Labs, an oncology healthcare AI company. "
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
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/hub/{filepath:path}")
def serve_hub_static(filepath: str):
    path = os.path.join(BASE_DIR, filepath)
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"error": "Not found"}, 404)
