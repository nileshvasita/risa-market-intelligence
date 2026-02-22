# RISA Labs - US Oncology Market Intelligence

> Interactive visualizations and intelligence platform for the US oncology ecosystem.

## 📊 Live Visualizations

Hosted on GitHub Pages - no setup needed:

| Visualization | Description |
|--------------|-------------|
| **[Hub](https://risa-labs-inc.github.io/risa-market-intelligence/)** | Master index of all visualizations |
| **[Money Flows](https://risa-labs-inc.github.io/risa-market-intelligence/money-flows.html)** | Every financial interaction with cancer care providers |
| **[Ecosystem Mind Map](https://risa-labs-inc.github.io/risa-market-intelligence/mindmap.html)** | Full US oncology stakeholder map |
| **[Workflows](https://risa-labs-inc.github.io/risa-market-intelligence/workflows.html)** | 120 workflows across 3 cancer centers (by department + patient journey) |
| **[Cancer Centers](https://risa-labs-inc.github.io/risa-market-intelligence/cancer-centers.html)** | 178 centers across CA, TX, WA |

## 🧠 Market Intelligence Hub (Local App)

An interactive platform with a structured database, REST APIs, and AI-powered chatbot for querying oncology market intelligence.

### What's in the database

| Entity | Count | Key Fields |
|--------|-------|------------|
| Cancer Centers | 178 | Name, city, state, category, parent org, EHR vendor, bed count, 340B status, annual cases |
| Market Segments | 43 | Segment name, role, pain points, RISA opportunity, money/data flows |
| Key Organizations | 126 | Pharma, payers, tech vendors, diagnostics, GPOs |
| Content Chunks | 197 | Full-text searchable research content |

### Quick Start

```bash
cd hub
pip install -r requirements.txt
cp .env.example .env       # Add your Anthropic API key
chmod +x start.sh
./start.sh                 # Builds DB + starts server at http://localhost:8501
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/centers?state=&category=&search=` | Filter/search cancer centers |
| `GET` | `/api/segments?search=` | Market segments |
| `GET` | `/api/organizations?type=&search=` | Key organizations |
| `GET` | `/api/search?q=` | Full-text search across all content |
| `POST` | `/api/chat` | AI-powered Q&A (Claude + local data) |

### Chat Modes

The chatbot answers questions using two sources:
- **Local data** - your curated RISA market intelligence (prioritized)
- **Claude's general knowledge** - supplements when local data doesn't cover the topic

Answers clearly distinguish between internal data and general knowledge.

## 📁 Repo Structure

```
├── index.html                  # GitHub Pages landing page
├── cancer-centers.html         # Interactive centers visualization
├── money-flows.html            # Financial flows visualization
├── workflows.html              # Oncology workflows visualization
├── mindmap.html                # Ecosystem mind map
├── presentations/              # Research presentations
├── hub/                        # Market Intelligence Hub app
│   ├── server.py               # FastAPI server
│   ├── build_db.py             # Parses markdown → SQLite
│   ├── enrich_centers.py       # Adds EHR, beds, 340B data
│   ├── index.html              # Hub frontend (dark theme)
│   ├── start.sh                # Launch script
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # API key template
├── data/                       # Raw markdown research
│   ├── cancer-centers-3-states.md
│   ├── cancer-center-workflows.md
│   ├── cancer-centers-research-report.md
│   ├── us-oncology-market-map.md
│   ├── us-oncology-whimsical-mindmap.md
│   └── risa-advisory-board-parker-classification.md
└── .github/workflows/pages.yml # Auto-deploy to GitHub Pages
```

## 🔒 Security

- API keys are **never committed** - use `hub/.env` (gitignored)
- `.db` files are generated locally, not checked in
- Run `build_db.py` to rebuild from source markdown at any time

## Contributing

1. Create a branch from `main`
2. Make your changes
3. Open a PR - describe what changed and why
4. Merge after review

---

Built by [RISA Labs](https://risalabs.ai)
