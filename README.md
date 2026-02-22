# RISA Labs — US Oncology Market Intelligence

Interactive visualizations and intelligence platform for the US oncology ecosystem.

## Live Visualizations (GitHub Pages)
- **[Hub](https://risa-labs-inc.github.io/risa-market-intelligence/)** — Master index
- **[Money Flows](https://risa-labs-inc.github.io/risa-market-intelligence/money-flows.html)** — Financial interactions
- **[Ecosystem Mind Map](https://risa-labs-inc.github.io/risa-market-intelligence/mindmap.html)** — Stakeholder map
- **[Workflows](https://risa-labs-inc.github.io/risa-market-intelligence/workflows.html)** — 120 workflows across 3 cancer centers
- **[Cancer Centers](https://risa-labs-inc.github.io/risa-market-intelligence/cancer-centers.html)** — 178 centers (CA, TX, WA)

## Market Intelligence Hub (Local App)

An interactive platform with structured database, REST APIs, and AI-powered chatbot for querying oncology market intelligence.

### Features
- **178 cancer centers** with EHR vendors, bed counts, 340B status
- **43 market segments** with RISA opportunities and pain points
- **126 key organizations** (pharma, payers, tech, diagnostics)
- **Full-text search** across all research content
- **AI chatbot** — ask questions, get answers from local data + Claude's knowledge

### Quick Start
```bash
cd hub
pip install -r requirements.txt
cp .env.example .env  # Add your Anthropic API key
./start.sh            # Builds DB + starts server at http://localhost:8501
```

### API Endpoints
- `GET /api/centers?state=&category=&search=` — Filter cancer centers
- `GET /api/segments?search=` — Market segments
- `GET /api/organizations?type=&search=` — Key organizations
- `GET /api/search?q=` — Full-text search
- `POST /api/chat` — AI-powered Q&A

## Data Sources
Raw research in `data/` directory — markdown reports on cancer centers, workflows, market maps, and oncology ecosystem analysis.

Built by RISA Labs.
