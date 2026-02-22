# RISA Labs - US Oncology Market Intelligence

> Interactive intelligence platform for the US oncology ecosystem - cancer centers, stakeholders, workflows, market landscape, and learning tools.

## 🧠 Market Intelligence Hub

A full-stack platform with structured database, REST APIs, AI chatbot, and interactive visualizations for oncology market intelligence.

### What's in the database

| Entity | Count | Key Fields |
|--------|-------|------------|
| Cancer Centers | 327 | Name, city, state, category, parent org, EHR vendor, bed count, 340B status, annual cases, geocoded |
| Stakeholders | 127 | Name, title, organization, role type, department, LinkedIn, relevance to RISA |
| Organizations | 351 | Health systems, pharma, payers, tech vendors, diagnostics |
| Workflows | 305 | Department, patient journey stage, steps (1,516), stakeholder mappings (1,130) |
| Market Segments | 43 | 9 categories with pain points, RISA opportunities, money/data flows |
| Content Chunks | 197 | Full-text searchable research content |

### Coverage

- **6 states:** California (72), Texas (68), New York (55), Florida (52), Massachusetts (42), Washington (38)
- **EHR vendors:** Epic (72), Cerner (12), iKnowMed (9), MEDITECH (9), Flatiron OncoEMR (6)
- **Center types:** Hospital Systems (152), Community Practices (69), Academic Medical Centers (42), Specialty Centers (40), NCI-Designated (24)
- **Deep dives:** Stanford Health Care (45 stakeholders across 4 tiers)

### Hub Features

| Feature | Description |
|---------|-------------|
| **Cancer Centers** | Searchable/filterable table with detail modals, editable notes |
| **Interactive Map** | Leaflet.js US map with 327 color-coded markers, analytics panel |
| **Market Map** | 9 collapsible category groups covering the full oncology ecosystem |
| **Organizations** | Directory with type badges, linked people and centers |
| **People Directory** | 127 stakeholders with roles, relevance badges, org/center cross-linking |
| **Workflows** | 305 workflows in 3 view modes (Table, Cards, Journey Map) with step timelines |
| **AI Chat** | Claude-powered Q&A using local data + general knowledge fallback |
| **Full Search** | Cross-module search across centers, people, orgs, and content |
| **Tutor Hub** | Glossary (79 terms) + 5 learning paths with interactive quizzes |

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
| `GET` | `/api/centers/{id}` | Center detail with linked people |
| `GET` | `/api/segments?search=` | Market segments |
| `GET` | `/api/organizations?type=&search=` | Organizations directory |
| `GET` | `/api/organizations/{id}` | Org detail with linked people and centers |
| `GET` | `/api/people?search=&org=&role_type=` | Stakeholder directory |
| `GET` | `/api/workflows?department=&search=` | Workflows with steps and stakeholders |
| `GET` | `/api/search?q=` | Full-text search across all content |
| `POST` | `/api/chat` | AI-powered Q&A (Claude + local data) |
| `PUT` | `/api/centers/{id}/notes` | Update center notes |
| `PUT` | `/api/people/{id}/notes` | Update stakeholder notes |

### Tutor Hub

Built-in learning platform to deeply understand the oncology market:

- **Glossary:** 79 terms across 10 categories (RCM, Payers, Pharma, Technology, Clinical Ops, etc.) with "Why It Matters for RISA" context and linked related concepts
- **Learning Paths:** 5 structured paths, 19 modules, 24 interactive quiz questions
  - The Patient Journey (screening to survivorship)
  - Follow the Money (oncology economics)
  - The Decision Makers (who to sell to and how)
  - The Competitive Landscape (where RISA fits)
  - RISA in Context (putting it all together)

## 📊 Static Visualizations

Hosted on GitHub Pages:

| Visualization | Description |
|--------------|-------------|
| **[Hub](https://risa-labs-inc.github.io/risa-market-intelligence/)** | Landing page |
| **[Money Flows](https://risa-labs-inc.github.io/risa-market-intelligence/money-flows.html)** | Financial interactions in cancer care |
| **[Ecosystem Mind Map](https://risa-labs-inc.github.io/risa-market-intelligence/mindmap.html)** | Full US oncology stakeholder map |
| **[Workflows](https://risa-labs-inc.github.io/risa-market-intelligence/workflows.html)** | Workflow visualizations by department + patient journey |
| **[Cancer Centers](https://risa-labs-inc.github.io/risa-market-intelligence/cancer-centers.html)** | Interactive centers map |

## 📁 Repo Structure

```
├── README.md
├── TODO.md                     # Project roadmap and task tracking
├── index.html                  # GitHub Pages landing page
├── cancer-centers.html         # Static centers visualization
├── money-flows.html            # Financial flows visualization
├── workflows.html              # Oncology workflows visualization
├── mindmap.html                # Ecosystem mind map
├── presentations/              # Research presentations
├── hub/                        # Market Intelligence Hub app
│   ├── server.py               # FastAPI server with all API endpoints
│   ├── index.html              # Hub frontend (single-page, dark theme)
│   ├── glossary.json           # Tutor Hub glossary data (79 terms)
│   ├── learning_paths.json     # Tutor Hub learning paths (5 paths, 19 modules)
│   ├── build_db.py             # Parses markdown into SQLite
│   ├── enrich_centers.py       # Adds EHR, beds, 340B, geocoding
│   ├── geocode_centers.py      # Lat/lng geocoding for map
│   ├── populate_stakeholders.py # Initial stakeholder import
│   ├── populate_stanford_deep.py # Stanford 45-person deep dive
│   ├── import_workflows.py     # 305 workflows with steps and mappings
│   ├── add_new_states.py       # FL, NY, MA center data
│   ├── rebuild_all.py          # Master script - rebuilds entire DB from scratch
│   ├── start.sh                # Launch script
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # API key template
├── data/                       # Raw markdown research
│   ├── cancer-centers-3-states.md
│   ├── cancer-centers-FL-NY-MA.md
│   ├── cancer-center-workflows.md
│   ├── cancer-centers-research-report.md
│   ├── us-oncology-market-map.md
│   ├── us-oncology-whimsical-mindmap.md
│   └── risa-advisory-board-parker-classification.md
└── .github/workflows/pages.yml # Auto-deploy to GitHub Pages
```

## 🔒 Security

- API keys are **never committed** - use `hub/.env` (gitignored)
- `.db` files are generated locally via `rebuild_all.py`
- Production deployment: GCP Cloud Run with IAP (@risalabs.ai access only)

## Contributing

1. Create a branch from `main`
2. Make changes
3. Open a PR
4. Merge after review (branch protection: 1 approval required)

---

Built by [RISA Labs](https://risalabs.ai)
